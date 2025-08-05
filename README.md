# College Admission Agent (EAMCET + Agentic AI)

This project helps students find colleges in Telangana based on their EAMCET rank and preferred location. It also includes a chatbot that answers admission-related queries using IBM’s Granite foundation model (Agentic AI).

---

## Features

- Rank-Based College Recommender
  - Filters based on EAMCET rank (up to 200000)
  - District-wise coverage: Hyderabad, Warangal, Karimnagar, Nizamabad, Nalgonda, Medak, etc.

-  Agentic AI Chatbot (IBM Granite)
  - Ask: *“What is the admission process for JNTU?”*
  - Uses IBM watsonx.ai Granite Model via API

-  Optional RAG Module (LangChain) for PDF Q&A

---

## Dataset: `colleges.csv`

This file contains:
- College Name
- Location (Telangana-wide)
- Closing Rank
- Branch (CSE, ECE, IT, AI, etc.)

 Designed for EAMCET students up to 2 lakh rank.

---

##  How to Run

1. Clone the repo or download ZIP

```bash

