import os
import json
import pandas as pd
from anthropic import Anthropic

def isolate_variances(financials_df: pd.DataFrame, metrics_df: pd.DataFrame) -> list[dict]:
    """
    Agent 1 (Claude 3 Haiku): Ingests the EDGAR financials and identifies the top variances.
    Returns a strict JSON payload mapping suspect metrics to their dollar/percentage variance.
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    fin_csv = financials_df.to_csv(index=False)
    met_csv = metrics_df.to_csv(index=False)
    
    prompt = f"""
    You are an expert Financial Planning & Analysis (FP&A) agent.
    Review the following SEC EDGAR financials and derived analyst metrics.
    Identify the most significant period-over-period variance (either positive or negative).
    
    Financials:
    {fin_csv}
    
    Metrics:
    {met_csv}
    
    Focus on QoQ or YoY changes.
    """
    
    tools = [
        {
            "name": "report_variances",
            "description": "Report the most suspect accounts with their variances.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "suspect_accounts": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "ticker": {"type": "string", "description": "The tokenized ticker symbol"},
                                "metric_name": {"type": "string", "description": "The name of the metric that changed significantly"},
                                "delta": {"type": "number", "description": "The exact percentage or value delta claimed"}
                            },
                            "required": ["ticker", "metric_name", "delta"]
                        }
                    }
                },
                "required": ["suspect_accounts"]
            }
        }
    ]
    
    print("[Agent 1] Analyzing EDGAR financials for significant variances using Claude...")
    
    try:
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            tools=tools,
            tool_choice={"type": "tool", "name": "report_variances"},
            messages=[{"role": "user", "content": prompt}]
        )
        
        # The tool use block is inside response.content
        for block in response.content:
            if block.type == "tool_use":
                payload = block.input.get("suspect_accounts", [])
                
                if isinstance(payload, list) and len(payload) == 1 and isinstance(payload[0], str):
                    try:
                        payload = json.loads(payload[0])
                    except:
                        pass
                
                if isinstance(payload, str):
                    try:
                        payload = json.loads(payload)
                    except:
                        pass
                        
                # Defensive check in case the LLM double-nests the JSON object
                if isinstance(payload, dict) and "suspect_accounts" in payload:
                    payload = payload["suspect_accounts"]
                    
                # Ensure it's a list
                if not isinstance(payload, list):
                    payload = [payload] if payload else []
                    
                return payload
        return []
    except Exception as e:
        print(f"[Agent 1] Error during generation: {e}")
        return []
