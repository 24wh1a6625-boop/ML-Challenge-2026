import pandas as pd

base = r".\data\student_resource\dataset\train"

s1 = pd.read_csv(
    base + r"\train_source1.tsv",
    sep="\t",
    usecols=["entity_id", "business_name"]
)

s2 = pd.read_csv(
    base + r"\train_source2.tsv",
    sep="\t",
    usecols=["entity_id", "business_name"]
)

s3 = pd.read_csv(
    base + r"\train_source3.tsv",
    sep="\t",
    usecols=["entity_id", "business_name"]
)

gt = pd.read_csv(
    base + r"\train_ground_truth.tsv",
    sep="\t",
    usecols=["source1_entity_id", "matched_entity_ids"]
)

names = pd.concat([s2, s3], ignore_index=True).set_index("entity_id")["business_name"]
s1_names = s1.set_index("entity_id")["business_name"]

total = 0
exact = 0
containment = 0

for _, row in gt[gt["matched_entity_ids"].fillna("").ne("")].iterrows():
    source1_name = str(s1_names.get(row["source1_entity_id"], "")).strip().lower()

    for matched_id in str(row["matched_entity_ids"]).split(","):
        matched_name = str(names.get(matched_id, "")).strip().lower()

        total += 1

        if source1_name == matched_name:
            exact += 1

        if source1_name in matched_name or matched_name in source1_name:
            containment += 1

print("Ground-truth matched pairs:", total)
print("Exact raw-name matches:", exact)
print("Exact-name rate:", round(exact / total, 4))
print("Containment matches:", containment)
print("Containment rate:", round(containment / total, 4))
