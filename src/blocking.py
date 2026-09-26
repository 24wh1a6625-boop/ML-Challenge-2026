from collections import defaultdict
from src.normalize import normalize_text


def tokenize(text):
    return set(normalize_text(text).split())


def build_indexes(target_rows):
    name_index = defaultdict(set)
    address_index = defaultdict(set)

    name_frequency = defaultdict(int)
    address_frequency = defaultdict(int)

    rows = list(target_rows)

    # Count name-token frequencies
    for row in rows:
        for token in tokenize(row["business_name"]):
            name_frequency[token] += 1

    # Count address-token frequencies
    for row in rows:
        for token in tokenize(row["business_address"]):
            address_frequency[token] += 1

    # Ignore extremely common tokens.
    # They create huge candidate sets and add little information.
    allowed_name_tokens = {
        token
        for token, count in name_frequency.items()
        if 2 <= count <= 1000
    }

    allowed_address_tokens = {
        token
        for token, count in address_frequency.items()
        if 2 <= count <= 1000
    }

    for row in rows:
        entity_id = row["entity_id"]

        name = normalize_text(row["business_name"])
        address = normalize_text(row["business_address"])

        if name:
            name_index[name].add(entity_id)

        if address:
            address_index[address].add(entity_id)

    name_token_index = defaultdict(set)
    address_token_index = defaultdict(set)

    for row in rows:
        entity_id = row["entity_id"]

        for token in tokenize(row["business_name"]) & allowed_name_tokens:
            name_token_index[token].add(entity_id)

        for token in tokenize(row["business_address"]) & allowed_address_tokens:
            address_token_index[token].add(entity_id)

    return {
        "name": dict(name_index),
        "address": dict(address_index),
        "name_token": dict(name_token_index),
        "address_token": dict(address_token_index),
    }


def generate_candidates(source1_row, indexes):
    candidates = set()

    name = normalize_text(source1_row["business_name"])
    address = normalize_text(source1_row["business_address"])

    # Route 1: exact normalized name
    if name:
        candidates.update(indexes["name"].get(name, set()))

    # Route 2: exact normalized address
    if address:
        candidates.update(indexes["address"].get(address, set()))

    # Route 3: informative name tokens
    for token in tokenize(source1_row["business_name"]):
        candidates.update(
            indexes["name_token"].get(token, set())
        )

    # Route 4: informative address tokens
    for token in tokenize(source1_row["business_address"]):
        candidates.update(
            indexes["address_token"].get(token, set())
        )

    return candidates