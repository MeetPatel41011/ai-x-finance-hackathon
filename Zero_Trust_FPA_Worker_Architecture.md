# Project Name: Zero-Trust Autonomous FP&A Worker

## 1. Hackathon Track Information
**Track:** MAXIMOR TRACK: MONEY OPERATIONS - EXPLAIN THE CHANGE

**The Problem:**
Build an AI agent that explains financial changes across multiple periods.
Given simple inputs such as:
* Monthly account summaries
* Transaction-level CSVs

**Requirements:**
Your agent should:
1. Compare financial results across periods
2. Identify the most meaningful variances
3. Drill into transaction-level data to find the key drivers
4. Produce a concise, evidence-backed explanation of what changed and why

**What Makes a Strong Submission?**
The strongest agents don’t just analyze one dataset once. They iterate on the input data, learn from previous runs, and build intuition around the underlying business context over multiple agent runs.

Your goal is to move from:
*"Revenue increased 18%."*
to:
*"Revenue increased 18%, primarily driven by a 32% increase in enterprise accounts, with three customers accounting for 64% of the increase."*

Build an agent that can answer: What changed? Why did it change? What is driving it?
*Note: Use own synthetic datasets.*

---

## 2. Proposed System Architecture

### Overview
A multi-agent consensus system that ingests financial CSVs, identifies account variances, and explains root causes without leaking sensitive enterprise data or hallucinating numbers.

### End-to-End Pipeline

#### 1. Ingress Sanitization (Data Privacy Layer)
* **Role:** Redact proprietary PII, employee payroll, customer names, and bank accounts into tokens (e.g., `<CLIENT_A>`).
* **Implementation:** Deterministic Python Regex + Local NER (`spaCy` or a lightweight local quantized model). Uses an ephemeral local Hash Map to store mappings. Data never leaves the local environment.

#### 2. Agent 1: Variance Isolation
* **Role:** Ingest sanitized multi-period summaries to calculate the largest dollar and percentage movers.
* **Implementation:** Fast LLM (Gemini 1.5 Flash / Claude 3.5 Haiku) paired with local Python data manipulation (pandas/DuckDB) to handle exact table math.

#### 3. Concurrent Execution (The Circuit Breaker Pattern)
*This is the core technical differentiator. Once Agent 1 identifies a variance, it forks the workflow into two parallel tasks using Python's `asyncio`.*

* **Task A - Agent 2 (Causal Driver Forensic):** A deep-reasoning LLM (e.g., Gemini 1.5 Pro or GPT-4o) groups transactions to find root causes. It integrates the **Tavily Search API** to fetch external macro events (e.g., inflation indices, supply chain news) explaining the variance.
* **Task B - Parallel Evaluator (Audit):** A deterministic Python worker mathematically verifies the transaction sums against the macro balance sheet variance.
* **The Circuit Breaker (`asyncio.Event`):** If the Evaluator detects that the transaction-level numbers fail reconciliation, it instantly raises an `ABORT_SIGNAL`. Agent 2's LLM generation is canceled mid-flight to prevent hallucination cascades, and the system falls back to re-filtering the data.

#### 4. Agent 3: Context Synthesizer
* **Role:** Turn raw findings into executive narratives, learning from prior cycles.
* **Implementation:** LLM utilizing a vector or episodic memory store to index explanations from prior runs, ensuring it doesn't repeat generic insights across quarters.

#### 5. Egress Sanitization (Re-hydration)
* **Role:** Swap tokens back into actual company and vendor names for presentation.
* **Implementation:** Local deterministic re-hydrator pulling directly from Stage 1's Hash Map.

---

## 3. Implementation Instructions for Antigravity (Coding Assistant)

**Phase 1: Synthetic Data Generation**
* Create a Python script using `pandas` and `Faker` to generate realistic multi-period monthly account summaries and transaction-level CSVs. Inject deliberate variances (e.g., a sudden 40% spike in cloud infrastructure costs, or a drop in a specific product's revenue).

**Phase 2: Sanitization Layer**
* Build the bidrectional tokenizer. Create `sanitize(dataframe)` and `rehydrate(text, token_map)` functions.

**Phase 3: Async Multi-Agent Framework**
* Scaffold the `asyncio` loop for the Agent 1 -> (Agent 2 + Evaluator) pipeline. 
* Implement the `asyncio.Event()` cancellation logic robustly so that HTTP requests to LLMs are actively terminated if the deterministic math check fails.

**Phase 4: Tool Calling**
* Integrate `TavilyClient` for web search. 
* Set up API connections for the parallel execution of the required LLMs to simulate the consensus routing.

**Phase 5: Output & UI**
* Format the final output as a clean, CFO-ready executive brief, ideally served via a lightweight FastAPI backend.
