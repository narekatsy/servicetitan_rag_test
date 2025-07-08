import json
from collections import Counter, defaultdict
import numpy as np

# Load logs
with open('logs.json', 'r') as f:
    logs = json.load(f)

# Metrics
thumbs_up = 0
thumbs_down = 0
latencies = []
bad_latency_queries = []
retrieval_sources_counter = Counter()
bad_retrieval_sources_counter = Counter()
retrieval_scores_good = []
retrieval_scores_bad = []

# For data source vs feedback
source_feedback = defaultdict(lambda: {'thumb_up': 0, 'thumb_down': 0})

for entry in logs:
    latency = entry["response_latency_ms"]
    latencies.append(latency)

    feedback = entry["user_feedback"]
    sources = [chunk["source"] for chunk in entry["retrieved_chunks"]]
    scores = [chunk["retrieval_score"] for chunk in entry["retrieved_chunks"]]

    for source in sources:
        retrieval_sources_counter[source] += 1
        source_feedback[source][feedback] += 1

    if feedback == "thumb_up":
        thumbs_up += 1
        retrieval_scores_good.extend(scores)
    else:
        thumbs_down += 1
        retrieval_scores_bad.extend(scores)
        if latency > 3500:
            bad_latency_queries.append(entry)

source_scores = defaultdict(lambda: {'good': [], 'bad': []})

for entry in logs:
    feedback = entry["user_feedback"]
    for chunk in entry["retrieved_chunks"]:
        score = chunk["retrieval_score"]
        source = chunk["source"]
        if feedback == "thumb_up":
            source_scores[source]['good'].append(score)
        else:
            source_scores[source]['bad'].append(score)

# Results
print(f"Total queries: {len(logs)}")
print(f"Thumbs Up: {thumbs_up}")
print(f"Thumbs Down: {thumbs_down}")
print(f"Bad Feedback Rate: {thumbs_down/len(logs)*100:.2f}%")

print("\nAvg Latency: {:.2f} ms".format(np.mean(latencies)))
print("P50 Latency: {:.2f} ms".format(np.percentile(latencies, 50)))
print("P95 Latency: {:.2f} ms".format(np.percentile(latencies, 95)))
print("P99 Latency: {:.2f} ms".format(np.percentile(latencies, 99)))

print("\nRetrieved Source Counts:")
for source, count in retrieval_sources_counter.items():
    print(f"  {source}: {count}")

print("\nRetrieved Source Feedback Breakdown:")
for source, fb in source_feedback.items():
    total = fb['thumb_up'] + fb['thumb_down']
    bad_pct = fb['thumb_down'] / total * 100 if total else 0
    print(f"  {source}: 👍 {fb['thumb_up']}, 👎 {fb['thumb_down']} (Bad %: {bad_pct:.2f}%)")

print("\nAverage Retrieval Score - Good Feedback: {:.3f}".format(np.mean(retrieval_scores_good)))
print("Average Retrieval Score - Bad Feedback: {:.3f}".format(np.mean(retrieval_scores_bad)))

print("\nAverage Retrieval Scores by Source:")
for source, scores in source_scores.items():
    good_avg = np.mean(scores['good']) if scores['good'] else 0
    bad_avg = np.mean(scores['bad']) if scores['bad'] else 0
    print(f"  {source}: 👍 {good_avg:.3f} | 👎 {bad_avg:.3f}")

print(f"\nQueries with Bad Feedback AND Latency > 3500ms: {len(bad_latency_queries)}")
