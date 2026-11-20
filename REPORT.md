# NVIDIA (NVDA) — Agent-Team Financial Report

**Author:** Austin (BSc Computer Science + Data Science, University of Sydney)  
**Company:** NVIDIA CORP (NASDAQ: NVDA, CIK 1045810)  
**Fiscal years covered:** FY2022-FY2026 (year ends in January; FY2026 ended 2026-01-25)  
**Market price:** $128.80 as of Nov 20, 2026 5:05 PM ET (Nasdaq)  
**Status:** educational exercise — not investment advice.

## How the agent team worked

| Agent | Main work | Output |
|---|---|---|
| Financial Data | Read 10-K / 10-Q via the SEC EDGAR company-facts API | Standardised financial data |
| Fundamental | Revenue, profit margin, cash flow, debt | Financial health assessment |
| Industry | Market size, competitors, moat | Industry competition analysis |
| Valuation | DCF, P/E, EV/EBITDA | Reasonable valuation range |
| Risk | Debt, dilution, regulation, competition risks | Risk list and Bear Case |
| Investment Analyst | Integrate all agents | Final investment judgement |
| Orchestrator | Allocate tasks, coordinate, check results, integrate | This report |

## 1. Financial data (from SEC filings)

Sources: SEC EDGAR company-facts API `https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json`; latest FY2026 10-K filed 2026-02-25 (accession 0001045810-26-000021); market price from the Nasdaq quote API `https://api.nasdaq.com/api/quote/NVDA/info?assetclass=stocks`.

| FY | Revenue | Gross profit | Operating income | Net income | Op. cash flow | CapEx | R&D |
|---|---|---|---|---|---|---|---|

| FY2022 | $26.9bn | $17.5bn | $10.0bn | $9.8bn | $9.1bn | $1.0bn | $5.3bn |

| FY2023 | $27.0bn | $15.4bn | $4.2bn | $4.4bn | $5.6bn | $1.8bn | $7.3bn |

| FY2024 | $60.9bn | $44.3bn | $33.0bn | $29.8bn | $28.1bn | $1.1bn | $8.7bn |

| FY2025 | $130.5bn | $97.9bn | $81.5bn | $72.9bn | $64.1bn | $3.2bn | $12.9bn |

| FY2026 | $215.9bn | $153.5bn | $130.4bn | $120.1bn | $102.7bn | $6.0bn | $18.5bn |


Latest reported: Q2 FY2027 ended 2026-07-26 (cumulative year-to-date) (filed 2026-08-26) — revenue $177.8bn, net income $118.0bn (cumulative year-to-date); standalone quarter revenue $96.2bn, net income $59.7bn.

## 2. Fundamental assessment

Revenue CAGR FY2022-FY2026: **68.3%**; net income CAGR: **87.3%**. Net cash at FY2026 year-end: **$40.7bn** (cash + marketable securities minus debt); current ratio 3.91; debt-to-equity 0.06.

| FY | Revenue growth | Gross margin | Operating margin | Net margin | R&D intensity | FCF |
|---|---|---|---|---|---|---|

| FY2022 | n/a | 64.9% | 37.3% | 36.2% | 19.6% | $8.1bn |

| FY2023 | 0.2% | 56.9% | 15.7% | 16.2% | 27.2% | $3.8bn |

| FY2024 | 125.9% | 72.7% | 54.1% | 48.8% | 14.2% | $27.0bn |

| FY2025 | 114.2% | 75.0% | 62.4% | 55.8% | 9.9% | $60.9bn |

| FY2026 | 65.5% | 71.1% | 60.4% | 55.6% | 8.6% | $96.7bn |

- Gross margin above 60% in FY2026 — pricing power, not a commodity cost structure.

- Net margin above 50% in FY2026 — unusually profitable even for a large-cap tech company.

- Revenue grew at a 68% CAGR over FY2022-FY2026 — the growth is real but historically extreme, so it cannot be extrapolated safely.

- Net cash of $40.7bn at FY2026 year-end (cash + marketable securities minus debt) — no solvency concern on the balance sheet.

- FY2023 revenue was almost flat (+0.2%) and operating cash flow fell — the business is cyclical, not a straight line up.


## 3. Industry and competition

A dominant position in a fast-growing but cyclical market: revenue CAGR 68% (FY2022-FY2026), gross margin 71.1% in FY2026, funded by R&D that itself compounds. The moat looks real, but it is a single-wave moat — the FY2023 slowdown is the reminder.

- Scale + switching costs: data-centre customers build systems, software (CUDA) and models around NVIDIA's platform; changing supplier means re-engineering, which is why gross margin stayed above 70% in FY2026.

- R&D engine: R&D spend rose from $5.3bn (FY2022) to $18.5bn (FY2026), a 37% CAGR — the moat is funded every year, not a one-off patent.

- Counterweight: that moat is tied to one demand wave (AI data-centre spending). FY2023 shows the cycle: revenue growth slowed to 0.2% and operating cash flow fell, before the AI wave lifted FY2024-FY2026.


Not available from the sources pulled (not estimated):

- Segment revenue split (Compute & Networking vs Graphics) — not present in the SEC company-facts file used here.

- Total addressable market size / market share — no independent source was pulled; not estimated.

- Peer financials — no peer filings were pulled in this project.


## 4. Valuation

### DCF (base case)

Base free cash flow: FY2026 FCF **$96.7bn**. Assumptions: FCF growth **12%** a year for 5 years, discount rate **10%**, terminal growth **3%**. Forecast FCF ($bn): 108.3, 121.3, 135.8, 152.1, 170.4. Enterprise value **$2,067.0bn**, equity value **$2,107.7bn**, value per share **$86.72**.

### Sensitivity — value per share ($) by discount rate (rows) and terminal growth (columns)

| Discount \ Terminal | 2% | 3% | 4% |
|---|---|---|---|

| 9% | $89.66 | $101.48 | $118.03 |

| 10% | $78.17 | $86.72 | $98.12 |

| 11% | $69.25 | $75.67 | $83.91 |


Sensitivity range: **$69.25 - $118.03** per share.

### FCF-growth scenarios (base discount 10%, terminal growth 3%)

| FCF growth | Value per share |
|---|---|

| 8% | $73.90 |

| 12% | $86.72 |

| 16% | $101.39 |


### Multiples (FY2026, price as above)

- P/E: **26.3x** (EPS diluted $4.90)
- EV/EBITDA: **23.2x** (EBITDA $133.2bn)
- EV/FCF: **32.0x**
- Market cap: **$3,130.5bn** on 24.30bn shares outstanding

## 5. Risks and Bear Case

- **Valuation risk — the price already assumes a lot of growth** (high): At $128.80 (as of Nov 20, 2026 5:05 PM ET), the share price is 49% above this project's DCF base case ($86.72). The DCF only reaches the current price if FCF grows well above 12% a year or the discount rate is well below 10%.

- **Demand cyclicality — the AI wave can pause, as it did in FY2023** (high): Revenue growth was 0.2% in FY2023 and operating cash flow fell from $9.1bn (FY2022) to $5.6bn (FY2023). A pause in data-centre spending would hit revenue, margins and FCF at once.

- **Customer concentration** (medium): A few hyperscale customers buy most data-centre GPUs. The exact share is not in the XBRL facts pulled here, so it is flagged qualitatively, not quantified. Losing or delaying one large customer matters.

- **Competition and custom silicon** (medium): AMD competes directly, and large cloud customers design their own AI chips. No peer financials were pulled, so this is a qualitative risk; the defence is R&D spend, which rose to $18.5bn in FY2026.

- **Export controls and geopolitics (qualitative)** (medium): US export controls on advanced chips to China are a known, recurring risk for NVIDIA. This project does not estimate the revenue at stake.

- **Dilution / share-based compensation** (low): Shares outstanding fell from 24.64bn (FY2024) to 24.30bn (FY2026) — buybacks more than offset dilution over this window, but that depends on buybacks continuing.


**Bear Case:** FCF growth 8% (vs 12% base), discount rate 11% (vs 10%), terminal growth 2% (vs 3%). Value per share **$59.32**, -54% vs the market price. AI data-centre spending pauses for a year, growth slows, and investors demand a higher return for the risk. FCF still grows, but the price paid today would be well above even a cautious fair value.

## 6. Final investment judgement (Investment Analyst)

Strong business, demanding price. At $128.80 the market price is above even the top of this DCF sensitivity range ($69.25-$118.03), and 49% above the base case ($86.72). The business would have to grow faster than the 12% FCF growth assumed here — or be discounted at less than 10% — for the current price to equal the DCF value.

- Does well: Revenue CAGR 68% (FY2022-FY2026) with a 71.1% gross margin.

- Does well: Free cash flow of $96.7bn in FY2026, a 45% FCF margin.

- Does well: Net cash of $40.7bn — the balance sheet is not the risk.

- Would change the judgement: FCF growth sustained at about 22% a year for 5 years (vs 12% in the base case, at the same 10% discount rate) would be needed for the DCF to reach the current price — even 16% growth only gives $101.39 a share.

- Would change the judgement: A data-centre spending pause (the FY2023 pattern) would cut the DCF sharply — see the Bear Case.

- Would change the judgement: A lower discount rate (e.g. if rates fall) lifts every DCF value in the sensitivity table.


## Limitations

- The DCF is highly sensitive to its assumptions: the sensitivity table spans $69.25-$118.03 per share, and the growth scenarios move it further. Treat the base case as one scenario, not a price target.
- Market price is a single as-of snapshot (see date above); multiples move with the price.
- No segment split, market-size estimate or peer comparison is included, because those numbers were not in the sources pulled — they were not invented.
- The agents are deterministic rules over filing data, not an LLM: they cannot read management commentary, 10-K risk-factor text, or news.
- Fiscal years end in January; 'FY2026' means the year ended 2026-01-25.


*Educational exercise only. This is not investment advice, not a recommendation to buy or sell any security, and the DCF is only as good as its stated assumptions.*
