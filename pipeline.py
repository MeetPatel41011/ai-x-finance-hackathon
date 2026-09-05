import asyncio
import os
import json
import uuid
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from circuit_breaker import run_concurrent_phase
from sanitizer import DataSanitizer
from agent1_variance import isolate_variances
from agent2_forensic import investigate_drivers
from agent3_synthesizer import ContextSynthesizer

async def run_pipeline():
    print("==================================================")
    print("  🚀 ZERO-TRUST AUTONOMOUS FP&A WORKER STARTING   ")
    print("==================================================\n")
    
    session_id = str(uuid.uuid4())
    
    # 0. Load Memory
    memory_path = "memory.json"
    memory = {
        "run_history": [],
        "aliases": [],
        "thresholds": [],
        "corrections": [],
        "owners": []
    }
    if os.path.exists(memory_path):
        with open(memory_path, "r") as f:
            try:
                memory = json.load(f)
            except:
                pass
            
    run_count = len(memory.get("run_history", []))
    run_id = run_count + 1
    
    if run_id == 1:
        data_dir = "data/q1"
    elif run_id == 2:
        data_dir = "data/q2"
    else:
        data_dir = "data/q3"
        
    print(f"--- RUN {run_id} (Loading from {data_dir}) ---")

    if os.path.exists(f"{data_dir}/financials.csv") and os.path.exists(f"{data_dir}/metrics.csv") and os.path.exists(f"{data_dir}/news.csv"):
        print("1. Ingesting EDGAR CSV data...")
        financials_df = pd.read_csv(f"{data_dir}/financials.csv")
        metrics_df = pd.read_csv(f"{data_dir}/metrics.csv")
        news_df = pd.read_csv(f"{data_dir}/news.csv")
    else:
        print(f"1. [ERROR] EDGAR CSVs not found in {data_dir}!")
        return {"error": "CSVs not found"}

    # 1.5 Sanitization
    print("\n[Sanitizer] Masking sensitive PII (Tickers)...")
    sanitizer = DataSanitizer()
    clean_financials = sanitizer.sanitize_dataframe(financials_df, target_column='ticker')
    clean_metrics = sanitizer.sanitize_dataframe(metrics_df, target_column='ticker')
    clean_news = sanitizer.sanitize_dataframe(news_df, target_column='ticker')

    # 2. Agent 1 (Variance Isolation)
    print("\n2. Agent 1: Isolating Variances...")
    suspect_accounts = isolate_variances(clean_financials, clean_metrics, session_id=session_id)
    print(f"  [Agent 1 JSON Payload]: {suspect_accounts}")

    if not suspect_accounts:
        print("No significant variances found. Exiting.")
        return {"error": "No significant variances found"}

    # 3. Concurrent Execution (Agent 2 + Evaluator)
    print("\n3. Launching Concurrent Tasks (Circuit Breaker Pattern)...")
    
    async def run_agent2():
        return await investigate_drivers(suspect_accounts, clean_news, clean_financials, session_id=session_id)

    raw_forensic_report = await run_concurrent_phase(suspect_accounts, clean_metrics, run_agent2)
    
    # Catch abort signal
    if "aborted" in raw_forensic_report.lower():
        print("\n" + raw_forensic_report)
        return {"error": raw_forensic_report}

    # 4. Agent 3 (Context Synthesizer)
    print("\n4. Agent 3: Synthesizing Executive Narrative...")
    synthesizer = ContextSynthesizer()
    final_narrative_masked = synthesizer.synthesize_narrative(raw_forensic_report, session_id=session_id)
    
    # 5. Rehydration
    print("\n[Sanitizer] Re-hydrating PII for final output...")
    final_narrative_clear = sanitizer.rehydrate_text(final_narrative_masked)
    
    # Re-hydrate the suspect accounts for the frontend
    rehydrated_accounts = []
    for acc in suspect_accounts:
        raw_ticker = acc.get('ticker', '')
        if isinstance(raw_ticker, str):
            clean = raw_ticker.strip("<>")
            actual_name = sanitizer.reverse_map.get(f"<{clean}>", raw_ticker)
            acc['ticker'] = actual_name
        rehydrated_accounts.append(acc)

    net_variance = sum(acc.get("delta", 0) for acc in rehydrated_accounts)
    
    external_signal = None
    if 'news_df' in locals() and not news_df.empty:
        first_news = news_df.iloc[0]
        external_signal = {
            "headline": first_news.get("summary", "No news found"),
            "source": first_news.get("source", "Unknown"),
            "date": first_news.get("date", "N/A"),
            "theme": first_news.get("theme", "N/A"),
            "entity": first_news.get("ticker", "N/A")
        }

    # --- MEMORY LEARNING SIMULATION ---
    memory["run_history"].append({
        "run": run_id,
        "flagged": len(suspect_accounts),
        "false_positives": max(0, len(suspect_accounts) - 1),
        "pct_explained": min(100, 70 + (run_id * 10))
    })
    
    if run_id == 1:
        memory["aliases"].append({"from": "NORTHWIND SYS LLC", "to": "Northwind Systems", "learned_run": 1})
    elif run_id == 2:
        memory["thresholds"].append({"account": "revenue_qoq", "pct": 12, "learned_run": 2})
        memory["owners"].append({"account": "revenue", "owner": "CFO Desk", "title": "Finance Team", "learned_run": 2})
    
    with open(memory_path, "w") as f:
        json.dump(memory, f, indent=2)

    payload = {
        "cfo_brief": final_narrative_clear,
        "variances": rehydrated_accounts,
        "net_variance": net_variance,
        "external_signal": external_signal,
        "memory": memory,
        "run_id": run_id,
        "quarter": f"2024Q{min(run_id, 3)}"
    }
    
    with open("run_data.json", "w") as f:
        json.dump(payload, f, indent=2)

    return payload
