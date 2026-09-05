# Instructions for the Data Intelligence Layer

Hey! This is the spec for **my part** of the project: the **Data Intelligence Layer** that feeds the earnings-analysis agent. Unlike the synthetic FP&A dataset, this layer ingests **real data** — quarterly earnings from SEC EDGAR + live news from Tavily — normalizes it, and hands the rest of the system one clean, typed object per company with provenance on every field.

**Core principle:** the layer's job is not to *explain* why revenue moved. It's to assemble the four evidence layers the agent needs to *adjudicate* that question — fact, claim, corroboration, and a numbers-check — each separately sourced and traceable.

---

## 0. What this is (and isn't)

- **This IS:** an open-world, real-data intelligence layer. Ground truth = reality. Numbers come from SEC XBRL (already reconciled/enforced by the SEC), news comes from the live web.
- **This is NOT:** synthetic data with a planted storyline. There's no pre-known "answer." Sometimes the honest output is *"management says demand, but margins say discounting."*
- **The hard part is taming messy real data** (missing fields, restatements, junk news, rate limits) — not authoring consistency. Handle that well and the layer is defensible.

---

## 1. Output Contract (the interface everyone builds against)

**JSON is the source of truth** (full fidelity, nested, with provenance). **CSV is a generated view** for download. Build JSON first, derive CSV from it — never the reverse.

Every data field follows this shape so downstream can cite and trust it:

```json
{
  "value": 35080000000,
  "source": "SEC EDGAR 10-Q",
  "url": "https://www.sec.gov/...",
  "as_of": "2025-08-27",
  "confidence": "high"
}
```

Missing data is expressed **explicitly**, never faked as 0:

```json
{ "value": null, "unavailable_reason": "XBRL concept not tagged for this filer" }
```

---

## 2. The Three Data Layers

### Layer A — Earnings & Financials (SEC EDGAR — ground truth)

- Resolve `ticker → CIK` via SEC `company_tickers.json`.
- Pull **both**: the **8-K earnings release** (Exhibit 99.1 — narrative + headline numbers, drops first) AND the **10-Q/10-K** (detailed XBRL financials + MD&A).
- Structured numbers via XBRL `companyconcept` API. Pull **this quarter vs. year-ago quarter** for each concept:
  - Revenue, Net income, Operating income, Gross profit, EPS, Operating cash flow, Total assets, Total liabilities, Cash, Long-term debt, Shares outstanding.
  - **Segment revenue** (high value — enables "which part drove the change").
- Also extract text sections: **MD&A** and **Risk Factors** (management's claimed causes, kept as attributed quotes — never paraphrased into asserted fact).

### Layer B — Derived / Analyst Metrics (where we add value)

Don't pass raw numbers through. Compute the analyst lens:

- **Growth:** Revenue & EPS YoY + QoQ; segment growth; accelerating vs. decelerating (4–8 quarter trend).
- **Quality-of-growth flags:** gross-margin trend (revenue up + margin down → discount-driven?), operating leverage, one-time vs. recurring.
- **Profitability:** gross / operating / net margin, ROE, ROIC.
- **Health:** current ratio, debt/equity, interest coverage, FCF, cash runway.
- **Valuation:** P/E, P/S, EV/EBITDA, PEG *(needs price — see §4 gap)*.
- **Surprise:** actual vs. consensus *(needs external estimates — see §4 gap)*.
- Ship **4–8 quarter time series**, not just point-in-time. Trends = intelligence.

### Layer C — News (Bloomberg-style crawl via Tavily)

Don't dump headlines. Structure for reasoning:

- **Targeted queries**, not generic: `{company} Q{n} earnings`, `{company} {top-moving-segment}`, `{company} guidance analyst reaction`, plus sector/macro context (competitor results, rates, FX).
- Per article extract: `source`, `date`, `url`, one-line `summary`, **`stance`** (bull/bear/neutral), **`relevance_to_quarter`** tag.
- **Cluster by theme** (demand, margins, competition, regulation) so agent gets *"3 sources on AI demand, 1 on customer concentration"* not 15 loose links.
- Dedupe; rank by source quality + recency; timestamp everything.

---

## 3. Pre-Cached Companies (demo safety + speed)

Pre-fetch and store these so demo time isn't spent crawling. **Freeze a specific quarter per company** and cache raw filings + XBRL + news alongside processed output (so a live re-crawl can't make the chosen insight vanish).

| Ticker | Why it's in the set |
|--------|--------------------|
| **NVDA** | Hero. Huge data-center growth vs. customer-concentration / margin tension. Rich segments + endless news. |
| **TSLA** | Best adjudication case: revenue up while margins fall (discount-driven vs. demand). Polarized news → stance tagging shines. |
| **NFLX** | Clean subs-vs-revenue story; ad tier / guidance beats & misses. |
| **JPM** | Non-tech, proves schema generalizes (net interest income, credit provisions). |
| **META** | Segment divergence (strong ads vs. Reality Labs losses). |

**Priority if short on time:** NVDA + TSLA + JPM airtight first (hero + tension + generality), then add NFLX + META. *Three polished beats five half-done.*

**Pre-verify the hero:** confirm TSLA's chosen quarter genuinely shows revenue-up / margin-down before demo. Don't discover a boring quarter on stage.

---

## 4. Red Flags — handle before they bite

- **SEC blocks you without a `User-Agent` header** (contact info required) and enforces ~10 req/sec. Set the header day one; cache aggressively. Silently kills demos otherwise.
- **Latency:** Tavily crawl + LLM per company = 15–60s+. **Never block the UI on a live crawl.** Pre-compute cached companies; return partial fast + enrich async for anything live.
- **Partial failure is normal, not exceptional.** Missing XBRL concept, junk news, no consensus. Emit explicit `null + reason`, never a fake 0.
- **Consensus / price gap:** EDGAR has NO stock price or analyst estimates → P/E, valuation multiples, and earnings surprise need an external free tier (Finnhub / yfinance / Alpha Vantage). **Decide now: source it or scope it out.** Don't discover this at hour 6.
- **XBRL comparability:** same concept across periods (filers switch tags), comparable period (duration vs. instant), watch restatements. This is what makes numbers quietly wrong — budget real time.

---

## 5. CSV Export (the download feature)

Data is hierarchical (time series + news list + provenance) and does **not** flatten into one CSV cleanly. Export as **related tables** in **long/tidy format**, keyed on `ticker` + `quarter`:

### `financials.csv` (long format — preserves time series)
| ticker | quarter | metric_name | value | unit | source | as_of | url |
|--------|---------|-------------|-------|------|--------|-------|-----|
| NVDA | 2025Q2 | revenue | 30040000000 | USD | 10-Q | 2025-08-27 | https://... |
| NVDA | 2025Q2 | gross_margin | 0.75 | ratio | derived | 2025-08-27 | — |

### `metrics.csv` (derived / analyst layer)
| ticker | quarter | metric_name | value | trend | flag |
|--------|---------|-------------|-------|-------|------|
| TSLA | 2024Q1 | revenue_yoy | -0.09 | decelerating | — |
| TSLA | 2024Q1 | gross_margin_delta_bps | -180 | down | discount_driven |

### `news.csv` (one row per article)
| ticker | quarter | date | source | stance | theme | summary | url |
|--------|---------|------|--------|--------|-------|---------|-----|
| TSLA | 2024Q1 | 2024-04-23 | Reuters | bear | margins | Price cuts pressure auto margin | https://... |

*JSON remains full-fidelity source of truth; CSVs are generated from it on export.*

---

## 6. What to hand the team FIRST

The **JSON schema + one filled-in sample company (NVDA)**. This unblocks the frontend (they build against the mock while I build the real pipeline) and forces every decision above to surface now instead of at demo time. Ship that before writing the full pipeline.

---

## 7. Definition of Done (per company)

- [ ] Latest 8-K + 10-Q/10-K located and parsed
- [ ] All XBRL financial concepts pulled, YoY + QoQ deltas computed
- [ ] Segment revenue extracted
- [ ] MD&A + risk factors captured as attributed quotes
- [ ] Derived metrics + quality-of-growth flags computed
- [ ] 4–8 quarter time series built
- [ ] Tavily news clustered, stance + theme tagged, deduped
- [ ] Every field has `value / source / url / as_of / confidence`
- [ ] Missing fields = explicit `null + reason`
- [ ] Exports cleanly to the 3 CSV tables
- [ ] Cached & frozen for demo
