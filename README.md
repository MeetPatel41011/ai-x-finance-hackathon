# Explain the Change: Autonomous FP&A Worker

This project was built for the **AI x Finance Hackathon (MAXIMOR TRACK: MONEY OPERATIONS)**.

Explain the Change is a Zero-Trust Autonomous FP&A (Financial Planning & Analysis) worker that explains financial changes across multiple periods. It automatically ingests quarterly data, isolates meaningful variances, conducts forensic investigations using LLMs, and synthesizes executive-ready CFO briefs.

## Key Features

1. **Multi-Agent Architecture**
   - **Agent 1 (Variance Agent):** Analyzes raw EDGAR financial datasets to identify significant period-over-period variances.
   - **Circuit Breaker (Deterministic Evaluator):** Intercepts Agent 1's claims and strictly audits the math against the raw CSV to ensure zero hallucinations.
   - **Agent 2 (Forensic Agent):** Investigates true anomalies by diving deep into MD&A context and external news to find causal drivers.
   - **Agent 3 (Synthesizer Agent):** Packages findings into an executive narrative.

2. **Stateful Memory & Learning**
   - The system maintains a `memory.json` state file across runs.
   - It intelligently learns aliases (e.g., mapping subsidiary names to parent names) and custom thresholds (e.g., ignoring variances below 12%) for future quarters.

3. **Zero-Trust Data Sanitization**
   - Implements a PII-scrubbing layer that tokenizes proprietary entities (e.g., `TSLA` -> `<CLIENT_001>`) before sending context to external LLM APIs, ensuring strict data privacy.

## Setup & Running

1. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn pandas anthropic
   ```

2. Configure environment variables in a `.env` file:
   ```env
   ANTHROPIC_API_KEY=your_key_here
   ```

3. Run the backend API:
   ```bash
   uvicorn app:app --port 8000
   ```

4. Open the UI:
   Open `Explain the Change prototype/Explain the Change.dc.html` in your browser via a local server (e.g., the 8000 port) to interact with the interactive dashboard.

## Repository Structure

- `data/q1`, `data/q2`, `data/q3`: Synthetic quarterly datasets (Ledger, Metrics, Plan).
- `app.py`: FastAPI backend entry point.
- `pipeline.py`: Core orchestration logic for the multi-agent pipeline.
- `circuit_breaker.py`: Deterministic guardrails for math checking.
- `sanitizer.py`: Data tokenization engine.
- `agent1_variance.py`, `agent2_forensic.py`, `agent3_synthesizer.py`: The specialized AI agents.
- `Explain the Change.dc.html`: The interactive React-based frontend dashboard.
