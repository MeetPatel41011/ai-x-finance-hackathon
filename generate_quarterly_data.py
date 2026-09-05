import os
import pandas as pd

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def generate_q1():
    out_dir = "data/q1"
    ensure_dir(out_dir)
    
    financials = pd.DataFrame([
        {"ticker": "TSLA", "quarter": "2024Q1", "metric_name": "revenue", "value": 21300000000.0, "unit": "USD", "source": "10-Q", "as_of": "2024-04-23", "url": "https://sec.gov"},
        {"ticker": "TSLA", "quarter": "2023Q4", "metric_name": "revenue", "value": 25170000000.0, "unit": "USD", "source": "10-K", "as_of": "2024-01-24", "url": "https://sec.gov"},
        {"ticker": "NVDA", "quarter": "2024Q1", "metric_name": "revenue", "value": 26040000000.0, "unit": "USD", "source": "10-Q", "as_of": "2024-05-22", "url": "https://sec.gov"},
        {"ticker": "NVDA", "quarter": "2023Q4", "metric_name": "revenue", "value": 22100000000.0, "unit": "USD", "source": "10-K", "as_of": "2024-02-21", "url": "https://sec.gov"},
        {"ticker": "NORTHWIND SYS LLC", "quarter": "2024Q1", "metric_name": "enterprise_revenue", "value": 1310400.0, "unit": "USD", "source": "internal", "as_of": "2024-04-23", "url": ""},
        {"ticker": "NORTHWIND SYS LLC", "quarter": "2023Q4", "metric_name": "enterprise_revenue", "value": 992000.0, "unit": "USD", "source": "internal", "as_of": "2024-01-24", "url": ""}
    ])
    
    metrics = pd.DataFrame([
        {"ticker": "TSLA", "quarter": "2024Q1", "metric_name": "revenue_qoq", "value": -0.153, "trend": "decelerating", "flag": "revenue_miss"},
        {"ticker": "NVDA", "quarter": "2024Q1", "metric_name": "revenue_qoq", "value": 0.178, "trend": "accelerating", "flag": "revenue_beat"},
        {"ticker": "NORTHWIND SYS LLC", "quarter": "2024Q1", "metric_name": "enterprise_revenue_qoq", "value": 0.321, "trend": "accelerating", "flag": "revenue_beat"}
    ])
    
    news = pd.DataFrame([
        {"ticker": "TSLA", "quarter": "2024Q1", "date": "2024-04-23", "source": "Reuters", "stance": "bear", "theme": "margins", "summary": "Price cuts pressure auto margin as TSLA attempts to spur demand.", "url": "https://news.com/tsla1"},
        {"ticker": "NORTHWIND SYS LLC", "quarter": "2024Q1", "date": "2024-04-20", "source": "Internal", "stance": "bull", "theme": "sales", "summary": "Northwind Systems signed 3 massive enterprise expansions.", "url": ""}
    ])
    
    financials.to_csv(f"{out_dir}/financials.csv", index=False)
    metrics.to_csv(f"{out_dir}/metrics.csv", index=False)
    news.to_csv(f"{out_dir}/news.csv", index=False)


def generate_q2():
    out_dir = "data/q2"
    ensure_dir(out_dir)
    
    financials = pd.DataFrame([
        {"ticker": "TSLA", "quarter": "2024Q2", "metric_name": "revenue", "value": 22500000000.0, "unit": "USD", "source": "10-Q", "as_of": "2024-07-23", "url": "https://sec.gov"},
        {"ticker": "TSLA", "quarter": "2024Q1", "metric_name": "revenue", "value": 21300000000.0, "unit": "USD", "source": "10-Q", "as_of": "2024-04-23", "url": "https://sec.gov"},
        {"ticker": "NVDA", "quarter": "2024Q2", "metric_name": "revenue", "value": 30040000000.0, "unit": "USD", "source": "10-Q", "as_of": "2024-08-22", "url": "https://sec.gov"},
        {"ticker": "NVDA", "quarter": "2024Q1", "metric_name": "revenue", "value": 26040000000.0, "unit": "USD", "source": "10-Q", "as_of": "2024-05-22", "url": "https://sec.gov"},
        {"ticker": "Northwind Systems", "quarter": "2024Q2", "metric_name": "enterprise_revenue", "value": 1450000.0, "unit": "USD", "source": "internal", "as_of": "2024-07-23", "url": ""},
        {"ticker": "Northwind Systems", "quarter": "2024Q1", "metric_name": "enterprise_revenue", "value": 1310400.0, "unit": "USD", "source": "internal", "as_of": "2024-04-23", "url": ""}
    ])
    
    metrics = pd.DataFrame([
        {"ticker": "TSLA", "quarter": "2024Q2", "metric_name": "revenue_qoq", "value": 0.056, "trend": "recovering", "flag": "revenue_in_line"},
        {"ticker": "NVDA", "quarter": "2024Q2", "metric_name": "revenue_qoq", "value": 0.153, "trend": "accelerating", "flag": "revenue_beat"},
        {"ticker": "Northwind Systems", "quarter": "2024Q2", "metric_name": "enterprise_revenue_qoq", "value": 0.106, "trend": "accelerating", "flag": "revenue_beat"}
    ])
    
    news = pd.DataFrame([
        {"ticker": "TSLA", "quarter": "2024Q2", "date": "2024-07-23", "source": "Bloomberg", "stance": "neutral", "theme": "deliveries", "summary": "Tesla deliveries stabilize but margins remain suppressed.", "url": "https://news.com/tsla3"}
    ])
    
    financials.to_csv(f"{out_dir}/financials.csv", index=False)
    metrics.to_csv(f"{out_dir}/metrics.csv", index=False)
    news.to_csv(f"{out_dir}/news.csv", index=False)


def generate_q3():
    out_dir = "data/q3"
    ensure_dir(out_dir)
    
    financials = pd.DataFrame([
        {"ticker": "TSLA", "quarter": "2024Q3", "metric_name": "revenue", "value": 24000000000.0, "unit": "USD", "source": "10-Q", "as_of": "2024-10-23", "url": "https://sec.gov"},
        {"ticker": "TSLA", "quarter": "2024Q2", "metric_name": "revenue", "value": 22500000000.0, "unit": "USD", "source": "10-Q", "as_of": "2024-07-23", "url": "https://sec.gov"},
        {"ticker": "NVDA", "quarter": "2024Q3", "metric_name": "revenue", "value": 32540000000.0, "unit": "USD", "source": "10-Q", "as_of": "2024-11-22", "url": "https://sec.gov"},
        {"ticker": "NVDA", "quarter": "2024Q2", "metric_name": "revenue", "value": 30040000000.0, "unit": "USD", "source": "10-Q", "as_of": "2024-08-22", "url": "https://sec.gov"},
        {"ticker": "Northwind Systems", "quarter": "2024Q3", "metric_name": "enterprise_revenue", "value": 1550000.0, "unit": "USD", "source": "internal", "as_of": "2024-10-23", "url": ""},
        {"ticker": "Northwind Systems", "quarter": "2024Q2", "metric_name": "enterprise_revenue", "value": 1450000.0, "unit": "USD", "source": "internal", "as_of": "2024-07-23", "url": ""}
    ])
    
    metrics = pd.DataFrame([
        {"ticker": "TSLA", "quarter": "2024Q3", "metric_name": "revenue_qoq", "value": 0.066, "trend": "recovering", "flag": "revenue_in_line"},
        {"ticker": "NVDA", "quarter": "2024Q3", "metric_name": "revenue_qoq", "value": 0.083, "trend": "accelerating", "flag": "revenue_beat"},
        {"ticker": "Northwind Systems", "quarter": "2024Q3", "metric_name": "enterprise_revenue_qoq", "value": 0.068, "trend": "steady", "flag": "revenue_in_line"}
    ])
    
    news = pd.DataFrame([
        {"ticker": "NVDA", "quarter": "2024Q3", "date": "2024-11-22", "source": "CNBC", "stance": "bull", "theme": "AI", "summary": "Nvidia Blackwell chips see unprecedented demand.", "url": "https://news.com/nvda3"}
    ])
    
    financials.to_csv(f"{out_dir}/financials.csv", index=False)
    metrics.to_csv(f"{out_dir}/metrics.csv", index=False)
    news.to_csv(f"{out_dir}/news.csv", index=False)

if __name__ == "__main__":
    generate_q1()
    generate_q2()
    generate_q3()
    print("Generated Q1, Q2, Q3 data.")
