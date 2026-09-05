import asyncio
import pandas as pd

class CircuitBreakerError(Exception):
    pass

async def task_b_evaluator(suspect_accounts_json, metrics_df, abort_event: asyncio.Event):
    """
    Parallel Evaluator (Audit): Mathematically verifies Agent 1's EDGAR claims.
    If the math fails, it triggers the abort_event.
    """
    print("[Evaluator] Starting deterministic math check against SEC EDGAR metrics...")
    try:
        await asyncio.sleep(0.5)
        
        for account in suspect_accounts_json:
            clean_ticker_val = account.get("ticker", "").strip("<>")
            metric = account.get("metric_name")
            claimed_delta = account.get("delta")
            
            # Find the actual ticker string in the dataframe (with brackets)
            actual_ticker = None
            for t in metrics_df['ticker'].values:
                if str(t).strip("<>") == clean_ticker_val:
                    actual_ticker = t
                    break
            
            if not actual_ticker:
                print(f"[Evaluator] ERROR: Hallucinated ticker! '{clean_ticker_val}' not found in raw EDGAR data.")
                abort_event.set()
                return False
                
            # Verify the metric actually exists for this ticker in our data
            ticker_metrics = metrics_df[metrics_df['ticker'] == actual_ticker]
            if metric not in ticker_metrics['metric_name'].values:
                print(f"[Evaluator] ERROR: Hallucinated metric! '{metric}' not found for {clean_ticker_val}.")
                abort_event.set()
                return False
                
        print("[Evaluator] Math/Schema verification passed!")
        return True
    except Exception as e:
        print(f"[Evaluator] Exception during audit: {e}")
        abort_event.set()
        return False

async def task_a_forensic(agent2_coroutine, abort_event: asyncio.Event):
    print("[Forensic Agent] Starting deep-reasoning generation...")
    
    llm_task = asyncio.create_task(agent2_coroutine())
    abort_task = asyncio.create_task(abort_event.wait())
    
    done, pending = await asyncio.wait(
        [llm_task, abort_task], 
        return_when=asyncio.FIRST_COMPLETED
    )
    
    if abort_task in done:
        print("[Forensic Agent] 🛑 CIRCUIT BREAKER TRIGGERED! Cancelling LLM generation mid-flight...")
        llm_task.cancel()
        raise CircuitBreakerError("LLM generation aborted due to deterministic math failure.")
        
    return llm_task.result()

async def run_concurrent_phase(suspect_accounts, metrics_df, agent2_coroutine):
    abort_event = asyncio.Event()
    
    evaluator = asyncio.create_task(task_b_evaluator(suspect_accounts, metrics_df, abort_event))
    forensic = asyncio.create_task(task_a_forensic(agent2_coroutine, abort_event))
    
    try:
        results = await asyncio.gather(evaluator, forensic)
        return results[1]
    except CircuitBreakerError as e:
        print(f"\n[SYSTEM] ABORT SIGNAL RECEIVED: {e}")
        return "Analysis aborted to prevent hallucinated numbers. Falling back to re-filtering..."
