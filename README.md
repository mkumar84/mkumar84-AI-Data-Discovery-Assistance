# 🔍 AI Data Discovery Assistant
# An LLM‑powered assistant that helps analysts find, understand, and explore enterprise data assets.

## 🧩 Overview
Large organizations often struggle with fragmented data ecosystems—multiple warehouses, inconsistent naming conventions, unclear ownership, and limited documentation. Analysts spend significant time searching for the right tables, columns, and metrics before they can even begin analysis.
The **AI Data Discovery Assistant** solves this by enabling natural‑language search and explanation of data assets. It acts as a smart layer on top of metadata, helping users quickly find relevant datasets, understand schema relationships, and accelerate time‑to‑insight.

## 🎯 Problem
Analysts and product teams face several challenges:
- Difficulty locating the right tables or fields across large data catalogs
- Lack of clear documentation or business definitions
- Slow onboarding for new analysts
- Repetitive questions to data engineering teams
- Fragmented metadata across systems
This leads to delays, inconsistent analysis, and duplicated work.

## 🚀 Goal
Build an AI assistant that enables:
- Natural‑language search for tables, columns, and metrics
- Explanations of data fields and relationships
- Metadata‑driven recommendations
- Faster onboarding and reduced dependency on SMEs

## 👤 My Role
- Defined user personas (analysts, PMs, data scientists)
- Mapped user intents (search, explain, compare, validate)
- Designed conversational flows and prompt strategies
- Defined metadata requirements and governance constraints
- Evaluated LLM output quality and hallucination risks
- Created a roadmap for enterprise integration

## 🛠 Approach
### 1. Metadata Ingestion
- Extracted table names, column names, descriptions, and lineage
- Normalized metadata for consistent search
- Created embeddings for semantic similarity
### 2. Intent Classification
- Search intent (“Find tables related to customer churn”)
- Explanation intent (“What does column X mean?”)
- Comparison intent (“Difference between revenue and net_revenue?”)
- Validation intent (“Is this field PII?”)
### 3. LLM‑Powered Responses
- Combined metadata retrieval with LLM reasoning
- Added guardrails to reduce hallucinations
- Provided structured responses (definitions, examples, lineage)

## 🧠 Architecture
User Query
    ↓
Intent Classifier
    ↓
Metadata Retriever → Embedding Search → Relevant Tables/Columns
    ↓
LLM Reasoning Layer (with guardrails)
    ↓
Final Answer (definitions, examples, recommendations)

### Core components:
- Metadata store
- Embedding search
- LLM prompt templates
- Guardrail logic
- Response formatter

## 💬 Example Interactions
**Query**
“Which tables contain customer churn information?”
**Response**
- **customer_churn_events** — Contains churn events with timestamps and churn reason codes.
- **customer_profile** — Includes churn risk score and customer attributes.
- **subscription_history** — Useful for analyzing churn patterns over time.

**Query**
“What does the field risk_score mean?”
**Response**
risk_score is a model‑generated metric representing the likelihood of customer churn within the next 90 days.
- Range: 0–1
- Higher values indicate higher churn probability
- Updated weekly based on behavioral and transactional features

## 📊 Evaluation
Evaluation focuses on:
- **Accuracy** — Does the assistant return the correct tables/fields?
- **Completeness** — Does it include all relevant metadata?
- **Clarity** — Are explanations understandable to non‑technical users?
- **Hallucination rate** — Does it avoid inventing fields or tables?
Planned evaluation enhancements:
- Automated hallucination detection
- Confidence scoring
- Metadata freshness indicators

## 🏁 Outcome
- Reduced analyst onboarding time
- Faster data discovery and exploration
- Fewer repetitive questions to data engineering
- Improved trust and adoption of data assets
- Foundation for enterprise‑wide data literacy

## 🔮 Roadmap
- Add RAG (Retrieval‑Augmented Generation) for grounding
- Add lineage visualization
- Add PII detection and data governance checks
- Add SQL generation from natural language
- Add usage analytics to improve recommendations
- Integrate with enterprise data catalogs (e.g., Collibra, Alation, Amundsen)

## 📁 Repository Structure
/data                 → Sample metadata  
/models               → Embedding and intent models  
/prompts              → LLM prompt templates  
/app                  → Assistant logic  
README.md             → Documentation  



## 🧑‍💼 Product Context
This project reflects real‑world challenges in enterprise data environments, especially in financial services and risk analytics. It aligns with your broader experience building AI‑enabled decision‑support tools and improving data accessibility across large organizations.


