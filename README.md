# Explain the Change: Autonomous FP&A Worker

This project was built for the **AI x Finance Hackathon (MAXIMOR TRACK: MONEY OPERATIONS)**.

## Problem Statement
Financial teams (FP&A) spend countless hours every quarter manually comparing financial results (like revenue or expenses) across multiple periods. When a significant variance occurs, analysts must painstakingly dig into transaction-level CSVs, cross-reference external news, and write up explanations for the CFO. This process is slow, prone to human error, and limits the time finance teams can spend on actual forward-looking strategy.

## Your Solution
**Explain the Change** is a Zero-Trust Autonomous FP&A worker. Given simple inputs like monthly account summaries and transaction-level CSVs, our AI agent automates the entire variance analysis workflow. It compares results across periods, identifies the most meaningful anomalies, drills into transaction-level data to find key business drivers, and produces a concise, evidence-backed CFO brief explaining exactly what changed and why. 

Crucially, it employs a **Circuit Breaker pattern** to mathematically verify LLM outputs, ensuring zero hallucination on financial figures.

## Key Features
1. **Multi-Agent Pipeline**: Specialized agents for Variance Isolation, Forensic Investigation, and Executive Synthesis.
2. **Mathematical Circuit Breaker**: Deterministic guardrails intercept LLM claims and audit the math strictly against the raw CSV. If an LLM hallucinates a number, the circuit breaks.
3. **Stateful Memory**: The system learns across runs. It remembers alias mappings (e.g., treating a subsidiary as the parent company) and materiality thresholds, cutting down on false positives in subsequent quarters.
4. **Live Data Chatbot**: An interactive Claude-powered Chatbot is built directly into the UI, allowing stakeholders to chat with the real-time financial data.
5. **Zero-Trust Data Sanitization**: Proprietary entity names (e.g., `TSLA`) are scrubbed and tokenized (e.g., `<CLIENT_001>`) before ever hitting the LLM API.

## Tech Stack
- **Backend**: Python, FastAPI, Pandas
- **AI / LLMs**: Anthropic Claude 3.5 Sonnet (via Hackathon API proxy), ChromaDB (for stateful memory vector embeddings)
- **Frontend**: HTML, CSS, JavaScript (React via CDN)

## How It Works
The pipeline orchestrates a flow of specialized tasks:
1. **Data Ingestion & Sanitization**: Raw CSVs from `data/q1` (or q2/q3) are ingested and PII is scrubbed.
2. **Agent 1 (Variance Isolation)**: Claude analyzes the financials to identify accounts that deviate significantly from expectations.
3. **Agent 2 (Forensic) & Evaluator**: Running concurrently, Agent 2 dives into MD&A and news to find the causal drivers of the variance, while the Evaluator strictly audits Agent 1's math.
4. **Agent 3 (Context Synthesizer)**: Drafts the final CFO brief using historical insights pulled from ChromaDB memory.
5. **UI Rendering**: The FastAPI backend sends the payload to a dynamic frontend dashboard where executives can read the brief and chat with the AI.

## How to run/use it

1. **Install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn pandas anthropic chromadb
   ```

2. **Configure API Keys**:
   Create a `.env` file in the root directory:
   ```env
   ANTHROPIC_API_KEY=your_key_here
   ```

3. **Start the Server**:
   ```bash
   uvicorn app:app --port 8000
   ```

4. **Open the Dashboard**:
   Open `http://127.0.0.1:8000/` in your browser.
   - Click the **"Run view"** button to execute the multi-agent pipeline on the current quarter's data.
   - Click the **"Chatbot"** button to ask follow-up questions about the variance analysis.

## Any other information
This project demonstrates how agentic AI can move beyond simple chat wrappers into true operational workflows. By implementing deterministic guardrails (the Circuit Breaker) and privacy-first design (Data Sanitization), we have built a tool that meets the strict compliance and accuracy standards required by enterprise finance teams.
