from collections import defaultdict

from src.normalize import normalize_text


def build_inverted_index(values):
    index = defaultdict(list)

    for entity_id, value in values:
        key = normalize_text(value)

        if key:
            index[key].append(entity_id)

    return dict(index)


def generate_candidates(source1_rows, source2_rows):
    name_index = build_inverted_index(
        (row["entity_id"], row["business_name"])
        for row in source2_rows
    )

    address_index = build_inverted_index(
        (row["entity_id"], row["business_address"])
        for row in source2_rows
    )

    candidates = {}

    for row in source1_rows:
        entity_id = row["entity_id"]

        candidate_ids = set()

        name_key = normalize_text(row["business_name"])
        address_key = normalize_text(row["business_address"])

        candidate_ids.update(name_index.get(name_key, []))
        candidate_ids.update(address_index.get(address_key, []))

        candidates[entity_id] = candidate_ids

    return candidates
