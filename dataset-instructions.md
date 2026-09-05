# Instructions for Synthetic Data Generation

Hey! We need a synthetic SaaS Revenue dataset to feed into the Zero-Trust Autonomous FP&A Worker. The agent will analyze this data to find anomalies, so we need to inject deliberate "storylines" for it to discover.

## Requirements

1. **Format:** Generate two CSV files:
   - `monthly_summaries.csv`: High-level aggregated data.
   - `transactions.csv`: Granular data mapping back to the summaries.

2. **Scale & Structure:**
   - **Timeframe:** 4 months of history (e.g., Jan to Apr 2024).
   - **Volume:** ~5,000 transactions per month.
   - **Clients:** 100 distinct client tokens (e.g., `Client_001`, `Client_002`).
   - **Columns (Transactions):** `Transaction_ID`, `Date`, `Client_ID`, `Type` (Upgrade, Downgrade, New, Churn, Renewal), `Amount`.
   - **Columns (Summaries):** `Month`, `Total_MRR`, `Total_Churn`, `Total_Upgrades`, etc.

3. **Injecting the "Storyline":**
   To test our agent's forensic capabilities, please inject a specific, mathematically sound narrative into the data. For example:
   - **Story 1:** In Month 3, `Client_042` and `Client_089` (two large Enterprise accounts) churn, causing a noticeable drop in total MRR.
   - **Story 2:** In Month 4, there is a massive 300% spike in upgrade revenue from just 5 specific clients.

*The Agent's job will be to read the summary, spot the variance, dive into the transactions, and explain EXACTLY which clients caused the shift. Make sure the math between the transactions and the summaries matches perfectly, as our Circuit Breaker will mathematically audit the agent's work!*
