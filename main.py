import asyncio
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from circuit_breaker import run_concurrent_phase
from sanitizer import DataSanitizer
from agent1_variance import isolate_variances
from agent2_forensic import investigate_drivers
from agent3_synthesizer import ContextSynthesizer

async def main():
    print("==================================================")
    print("  🚀 ZERO-TRUST AUTONOMOUS FP&A WORKER STARTING   ")
    print("==================================================\n")
    
    if os.path.exists("financials.csv") and os.path.exists("metrics.csv") and os.path.exists("news.csv"):
        print("1. Ingesting EDGAR CSV data...")
        financials_df = pd.read_csv("financials.csv")
        metrics_df = pd.read_csv("metrics.csv")
        news_df = pd.read_csv("news.csv")
    else:
        print("1. [ERROR] EDGAR CSVs not found! Please run generate_edgar_mock.py first.")
        return

    # 1.5 Sanitization
    print("\n[Sanitizer] Masking sensitive PII (Tickers)...")
    sanitizer = DataSanitizer()
    clean_financials = sanitizer.sanitize_dataframe(financials_df, target_column='ticker')
    clean_metrics = sanitizer.sanitize_dataframe(metrics_df, target_column='ticker')
    clean_news = sanitizer.sanitize_dataframe(news_df, target_column='ticker')

    # 2. Agent 1 (Variance Isolation)
    print("\n2. Agent 1: Isolating Variances...")
    suspect_accounts = isolate_variances(clean_financials, clean_metrics)
    print(f"  [Agent 1 JSON Payload]: {suspect_accounts}")

    if not suspect_accounts:
        print("No significant variances found. Exiting.")
        return

    # 3. Concurrent Execution (Agent 2 + Evaluator)
    print("\n3. Launching Concurrent Tasks (Circuit Breaker Pattern)...")
    
    async def run_agent2():
        return await investigate_drivers(suspect_accounts, clean_news, clean_financials)

    raw_forensic_report = await run_concurrent_phase(suspect_accounts, clean_metrics, run_agent2)
    
    # Catch abort signal
    if "aborted" in raw_forensic_report.lower():
        print("\n" + raw_forensic_report)
        return

    # 4. Agent 3 (Context Synthesizer)
    print("\n4. Agent 3: Synthesizing Executive Narrative...")
    synthesizer = ContextSynthesizer()
    final_narrative_masked = synthesizer.synthesize_narrative(raw_forensic_report)
    
    # 5. Rehydration
    print("\n[Sanitizer] Re-hydrating PII for final output...")
    final_narrative_clear = sanitizer.rehydrate_text(final_narrative_masked)
    
    print("\n==================================================")
    print("                FINAL CFO BRIEF                   ")
    print("==================================================")
    print(final_narrative_clear)
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(main())
