import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load logs
with open('logs.json') as f:
    logs = json.load(f)

# Convert to dataframe
data = []
for entry in logs:
    latency = entry["response_latency_ms"]
    feedback = entry["user_feedback"]
    avg_score = sum(chunk["retrieval_score"] for chunk in entry["retrieved_chunks"]) / len(entry["retrieved_chunks"])
    data.append({
        "latency": latency,
        "feedback": 1 if feedback == "thumb_up" else 0,  # 1 = good, 0 = bad
        "avg_retrieval_score": avg_score
    })

df = pd.DataFrame(data)

# ✅ Calculate correlations
cor_latency = df["latency"].corr(df["feedback"])
cor_score = df["avg_retrieval_score"].corr(df["feedback"])

print(f"Correlation between feedback and latency: {cor_latency:.3f}")
print(f"Correlation between feedback and avg retrieval score: {cor_score:.3f}")

# ✅ Visualize
sns.scatterplot(data=df, x="latency", y="avg_retrieval_score", hue="feedback")
plt.title("Latency vs Retrieval Score vs Feedback (1=Good, 0=Bad)")
plt.show()

# ✅ Also, boxplots to compare latency by feedback
sns.boxplot(data=df, x="feedback", y="latency")
plt.title("Latency by Feedback")
plt.xlabel("Feedback (1=Good, 0=Bad)")
plt.ylabel("Latency (ms)")
plt.show()
