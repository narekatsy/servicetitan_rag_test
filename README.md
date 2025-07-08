# ServiceTitan Data Science Internship Retrieval-Augmented Generation (RAG) Task

This repository contains my solution to the RAG system design exercise as part of the ServiceTitan internship selection process.



## Key Components

`logs.json`: Contains the logs data from recent user interactions with the chatbot.

`analyze_logs.py`: Analyzes user logs to summarize feedback, latency, and retrieval performance.

`latency_analysis.py`: Computes and visualizes how latency and retrieval scores relate to user feedback.


## Outputs

1. Output of `latency_analysis.py`

```bash
Correlation between feedback and latency: -0.438
Correlation between feedback and avg retrieval score: 0.629
```

2. Output of `analyze_logs.py`

```bash
Total queries: 81
Thumbs Up: 65  
Thumbs Down: 16
Bad Feedback Rate: 19.75%

Avg Latency: 3155.56 ms
P50 Latency: 2950.00 ms
P95 Latency: 4850.00 ms
P99 Latency: 5120.00 ms

Retrieved Source Counts:
  Archived Design Docs (PDFs): 89
  Engineering Wiki: 127
  Confluence: 108

Retrieved Source Feedback Breakdown:
  Archived Design Docs (PDFs): 👍 64, 👎 25 (Bad %: 28.09%)
  Engineering Wiki: 👍 108, 👎 19 (Bad %: 14.96%)
  Confluence: 👍 88, 👎 20 (Bad %: 18.52%)

Average Retrieval Score - Good Feedback: 0.920
Average Retrieval Score - Bad Feedback: 0.882

Average Retrieval Scores by Source:
  Archived Design Docs (PDFs): 👍 0.894 | 👎 0.897
  Engineering Wiki: 👍 0.936 | 👎 0.859
  Confluence: 👍 0.920 | 👎 0.885

Queries with Bad Feedback AND Latency > 3500ms: 10
```
