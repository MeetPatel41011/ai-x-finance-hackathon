import asyncio
import os
import pandas as pd
from anthropic import Anthropic

async def investigate_drivers(suspect_accounts: list[dict], news_df: pd.DataFrame, financials_df: pd.DataFrame) -> str:
    """
    Agent 2 (Claude 3.5 Sonnet): Deep-reasoning agent that finds the root cause of variances.
    It combines EDGAR financials with macro news data.
    Uses asyncio.to_thread to ensure the HTTP calls don't block the Circuit Breaker event loop.
    """
    if not suspect_accounts:
        return "No significant variances detected to investigate."
        
    print("[Forensic Agent] Pulling contextual news and MD&A quotes...")
    
    tickers = [str(acc.get('ticker', '')).strip('<>') for acc in suspect_accounts]
    
    if 'ticker' in news_df.columns:
        filtered_news = news_df[news_df['ticker'].astype(str).str.strip('<>').isin(tickers)]
    else:
        filtered_news = news_df
        
    if 'ticker' in financials_df.columns:
        filtered_fin = financials_df[financials_df['ticker'].astype(str).str.strip('<>').isin(tickers)]
    else:
        filtered_fin = financials_df
    
    news_csv = filtered_news.to_csv(index=False)
    fin_csv = filtered_fin.to_csv(index=False)
    
    prompt = f"""
    You are an elite forensic accountant. You need to explain WHY there was a massive variance in these accounts.
    
    Here are the raw financial metrics for the highly anomalous accounts:
    {fin_csv}
    
    Here is the macroeconomic news and MD&A context that explains external pressures on these clients:
    {news_csv}
    
    Provide a detailed forensic explanation of what drove the variance.
    Cite specific values, dates, and news sources. Focus heavily on the exact narrative.
    """
    
    print("[Forensic Agent] Generating causal explanation via Claude 3.5 Sonnet...")
    
    try:
        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        # Run synchronous generation in a separate thread so circuit breaker can cancel it mid-flight
        response = await asyncio.to_thread(
            client.messages.create,
            model='claude-sonnet-5',
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return "".join(block.text for block in response.content if hasattr(block, 'text'))
    except Exception as e:
        print(f"[Forensic Agent] Error during generation: {e}")
        return "Failed to generate forensic report."
