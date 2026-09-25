def f05_score(true_ids, predicted_ids):
    true_ids = set(true_ids)
    predicted_ids = set(predicted_ids)

    if not true_ids and not predicted_ids:
        return 1.0

    if not true_ids or not predicted_ids:
        return 0.0

    true_positive = len(true_ids & predicted_ids)

    precision = true_positive / len(predicted_ids)
    recall = true_positive / len(true_ids)

    if precision == 0 and recall == 0:
        return 0.0

    return (1.25 * precision * recall) / (0.25 * precision + recall)
def macro_f05_score(true_matches, predicted_matches):
    scores = []

    for source1_id, true_ids in true_matches.items():
        predicted_ids = predicted_matches.get(source1_id, [])
        scores.append(f05_score(true_ids, predicted_ids))

    if not scores:
        return 0.0

    return sum(scores) / len(scores)