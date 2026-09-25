import pandas as pd
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from src.normalize import normalize_text

base = r".\data\student_resource\dataset\train"

s1 = pd.read_csv(
    base + r"\train_source1.tsv",
    sep="\t",
    usecols=["entity_id", "business_name", "business_address"]
).set_index("entity_id")

s2 = pd.read_csv(
    base + r"\train_source2.tsv",
    sep="\t",
    usecols=["entity_id", "business_name", "business_address"]
)

s3 = pd.read_csv(
    base + r"\train_source3.tsv",
    sep="\t",
    usecols=["entity_id", "business_name", "business_address"]
)

targets = pd.concat([s2, s3], ignore_index=True).set_index("entity_id")

name_index = {}
address_index = {}

for entity_id, value in zip(targets.index, targets["business_name"]):
    key = normalize_text(value)
    if key:
        name_index.setdefault(key, set()).add(entity_id)

for entity_id, value in zip(targets.index, targets["business_address"]):
    key = normalize_text(value)
    if key:
        address_index.setdefault(key, set()).add(entity_id)

gt = pd.read_csv(
    base + r"\train_ground_truth.tsv",
    sep="\t",
    usecols=["source1_entity_id", "matched_entity_ids"]
)

gt = gt[gt["matched_entity_ids"].fillna("").ne("")]

covered = 0
total = 0

for row in gt.itertuples(index=False):
    source1 = s1.loc[row.source1_entity_id]

    name_key = normalize_text(source1["business_name"])
    address_key = normalize_text(source1["business_address"])

    candidates = (
        name_index.get(name_key, set())
        | address_index.get(address_key, set())
    )

    true_ids = set(row.matched_entity_ids.split(","))

    total += len(true_ids)
    covered += len(true_ids & candidates)

print("True matched pairs:", total)
print("Pairs retrieved by blocker:", covered)
print("Blocking recall:", round(covered / total, 4))
