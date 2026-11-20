# Agent-Team Financial Analysis — NVIDIA (NVDA)

## A summer-research / internship portfolio project

**Author:** Austin (BSc Computer Science + Data Science, University of Sydney)

A working version of an agent-team project that analyses a company's
financial reports and reaches an investment judgement. No LLM API key is
needed: each agent is a deterministic Python module with a clear role and a
structured output, so the whole pipeline runs offline except for downloading
the real filing data.

## What it does

Given NVIDIA (NASDAQ: NVDA), the team reads its real SEC filings and
produces a full investment report:

| Agent | Main work | Output |
|---|---|---|
| Financial Data | Read 10-K / 10-Q via the SEC EDGAR company-facts API | Standardised financial data |
| Fundamental | Revenue, profit margin, cash flow, debt | Financial health assessment |
| Industry | Market size, competitors, moat | Industry competition analysis |
| Valuation | DCF, P/E, EV/EBITDA | Reasonable valuation range |
| Risk | Debt, dilution, regulation, competition risks | Risk list and Bear Case |
| Investment Analyst | Integrate all agents | Final investment judgement |
| Orchestrator | Allocate tasks, coordinate, check results, integrate | This report |

## Results (verified run, 21 Nov 2026)

- Revenue FY2026: **$215.9bn**, up 65.5% year on year; revenue CAGR FY2022–FY2026: **68.3%**
- Gross margin FY2026: **71.1%**; net margin: **55.6%**; free cash flow: **$96.7bn**
- Net cash at FY2026 year-end: **$40.7bn** (cash + marketable securities minus debt)
- DCF base case: **$86.72 per share** (FCF growth 12% for 5 years, discount rate 10%, terminal growth 3%); sensitivity range **$69.25–$118.03**
- Market price: **$128.80** (Nasdaq, 20 Nov 2026, 5:05 PM ET) — above the top of the DCF range
- Bear Case: **$59.32 per share**
- Final judgement: **strong business, demanding price** — see `REPORT.md` for the reasoning. Educational exercise only, not investment advice.

Full numbers, tables and charts are in `REPORT.md` and `results/`.

## Data

Real data only — nothing is invented:

- **SEC EDGAR company-facts API** (free, no key):
  `https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json`
  (NVIDIA CORP, CIK 1045810; latest FY2026 10-K filed 2026-02-25)
- **Market price:** Nasdaq quote API
  `https://api.nasdaq.com/api/quote/NVDA/info?assetclass=stocks`
  (as-of date is recorded in the report)

The raw company-facts file is downloaded at run time (`data/companyfacts_nvda.json`,
git-ignored). The standardised 5-year table is saved as
`data/standardised_financials.csv`.

## Run it

```bash
bash run_all.sh          # creates .venv, installs deps, runs the pipeline
```

Individual steps:

```bash
.venv/bin/python src/run.py   # runs the Orchestrator, writes results/ + REPORT.md
```

## Files

| File | What it is |
|---|---|
| `src/financial_data.py` | Financial Data Agent: fetch + standardise SEC filings |
| `src/fundamental.py` | Fundamental Agent: margins, growth, cash flow, leverage |
| `src/industry.py` | Industry Agent: moat, competition, cycle |
| `src/valuation.py` | Valuation Agent: DCF, sensitivity, multiples |
| `src/risk.py` | Risk Agent: risk list + Bear Case |
| `src/investment_analyst.py` | Investment Analyst: final judgement |
| `src/orchestrator.py` | Orchestrator Agent: run + check all agents |
| `src/charts.py` | Chart helpers |
| `src/run.py` | Main entry point: results, report, charts |
| `REPORT.md` | Generated report (same numbers as `results/results.json`) |
| `results/` | `results.json`, `report.md`, `report.html`, 2 charts |

## Limitations (read before citing the numbers)

- The DCF is very sensitive to its assumptions — the sensitivity table spans
  $69.25–$118.03 a share. The base case is one scenario, not a price target.
- No segment split, market-size estimate or peer comparison is included:
  those numbers were not in the sources pulled, so they were not invented.
- The agents are deterministic rules over filing data, not an LLM: they cannot
  read management commentary, 10-K risk-factor text, or news.
- The market price is a single as-of snapshot; re-running the pipeline on
  another day will fetch a different price.
