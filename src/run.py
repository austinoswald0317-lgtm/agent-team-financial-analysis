"""Main entry point: run the Orchestrator, then write results + report + charts.

Usage:  python src/run.py        (from the project root, or anywhere)
Outputs: results/results.json, results/report.md, results/report.html,
         results/revenue_margin.png, results/valuation_range.png,
         REPORT.md (project root, generated from the same numbers),
         data/standardised_financials.csv
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import charts
import orchestrator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")


def _bn(x):
    return f"${x:,.1f}bn" if x is not None else "n/a"


def _pct(x):
    return f"{x:.1f}%" if x is not None else "n/a"


def _num(x, nd=2):
    return f"{x:,.{nd}f}" if x is not None else "n/a"


def build_report(r):
    d, f, ind, v, rk, an = (r["financial_data"], r["fundamental"], r["industry"],
                           r["valuation"], r["risk"], r["investment_analyst"])
    h = an["headline"]
    rows = d["annual_table"]
    price, as_of = d["price"]["price_usd"], d["price"].get("as_of")
    lines = []
    a = lines.append
    a("# NVIDIA (NVDA) — Agent-Team Financial Report\n")
    a("**Author:** Austin (BSc Computer Science + Data Science, University of Sydney)  \n"
      "**Company:** NVIDIA CORP (NASDAQ: NVDA, CIK 1045810)  \n"
      "**Fiscal years covered:** FY2022-FY2026 (year ends in January; FY2026 ended 2026-01-25)  \n"
      f"**Market price:** ${price:.2f} as of {as_of} (Nasdaq)  \n"
      "**Status:** educational exercise — not investment advice.\n")
    a("## How the agent team worked\n")
    a("| Agent | Main work | Output |\n|---|---|---|\n"
      "| Financial Data | Read 10-K / 10-Q via the SEC EDGAR company-facts API | Standardised financial data |\n"
      "| Fundamental | Revenue, profit margin, cash flow, debt | Financial health assessment |\n"
      "| Industry | Market size, competitors, moat | Industry competition analysis |\n"
      "| Valuation | DCF, P/E, EV/EBITDA | Reasonable valuation range |\n"
      "| Risk | Debt, dilution, regulation, competition risks | Risk list and Bear Case |\n"
      "| Investment Analyst | Integrate all agents | Final investment judgement |\n"
      "| Orchestrator | Allocate tasks, coordinate, check results, integrate | This report |\n")
    a("## 1. Financial data (from SEC filings)\n")
    a("Sources: SEC EDGAR company-facts API "
      "`https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json`; "
      "latest FY2026 10-K filed 2026-02-25 (accession 0001045810-26-000021); "
      "market price from the Nasdaq quote API "
      "`https://api.nasdaq.com/api/quote/NVDA/info?assetclass=stocks`.\n")
    a("| FY | Revenue | Gross profit | Operating income | Net income | Op. cash flow | CapEx | R&D |\n"
      "|---|---|---|---|---|---|---|---|\n")
    for row in rows:
        a(f"| FY{row['fiscal_year']} | {_bn(row['revenue']/1e9 if row['revenue'] else None)} | "
          f"{_bn(row['gross_profit']/1e9 if row['gross_profit'] else None)} | "
          f"{_bn(row['operating_income']/1e9 if row['operating_income'] else None)} | "
          f"{_bn(row['net_income']/1e9 if row['net_income'] else None)} | "
          f"{_bn(row['operating_cash_flow']/1e9 if row['operating_cash_flow'] else None)} | "
          f"{_bn(row['capex']/1e9 if row['capex'] else None)} | "
          f"{_bn(row['rd_expense']/1e9 if row['rd_expense'] else None)} |\n")
    q = d["latest_quarter"]
    a(f"\nLatest reported: {q['period']} (filed {q['filed']}) — revenue "
      f"{_bn(q['revenue_usd']/1e9 if q['revenue_usd'] else None)}, "
      f"net income {_bn(q['net_income_usd']/1e9 if q['net_income_usd'] else None)} "
      f"(cumulative year-to-date); standalone quarter revenue "
      f"{_bn(q['standalone_revenue_usd']/1e9 if q['standalone_revenue_usd'] else None)}, "
      f"net income {_bn(q['standalone_net_income_usd']/1e9 if q['standalone_net_income_usd'] else None)}.\n")
    a("## 2. Fundamental assessment\n")
    a(f"Revenue CAGR FY2022-FY2026: **{_pct(f['revenue_cagr_fy22_fy26_pct'])}**; "
      f"net income CAGR: **{_pct(f['net_income_cagr_fy22_fy26_pct'])}**. "
      f"Net cash at FY2026 year-end: **{_bn(f['leverage']['net_cash_usd_bn'])}** "
      f"(cash + marketable securities minus debt); current ratio "
      f"{_num(f['leverage']['current_ratio'])}; debt-to-equity "
      f"{_num(f['leverage']['debt_to_equity'])}.\n")
    a("| FY | Revenue growth | Gross margin | Operating margin | Net margin | R&D intensity | FCF |\n"
      "|---|---|---|---|---|---|---|\n")
    for fy in sorted(f["by_year"]):
        b = f["by_year"][fy]
        a(f"| FY{fy} | {_pct(b['revenue_growth_pct'])} | {_pct(b['gross_margin_pct'])} | "
          f"{_pct(b['operating_margin_pct'])} | {_pct(b['net_margin_pct'])} | "
          f"{_pct(b['rd_intensity_pct'])} | {_bn(b['fcf_usd_bn'])} |\n")
    for s in f["assessment"]:
        a(f"- {s}\n")
    a("\n## 3. Industry and competition\n")
    a(ind["conclusion"] + "\n")
    for m in ind["moat_assessment"]:
        a(f"- {m}\n")
    a("\nNot available from the sources pulled (not estimated):\n")
    for n in ind["not_available"]:
        a(f"- {n}\n")
    a("\n## 4. Valuation\n")
    va, m = v["assumptions"], v["multiples"]
    a("### DCF (base case)\n")
    a(f"Base free cash flow: FY2026 FCF **{_bn(v['fcf_fy2026_usd_bn'])}**. "
      f"Assumptions: FCF growth **{va['fcf_growth_5y_pct']:.0f}%** a year for 5 years, "
      f"discount rate **{va['discount_rate_pct']:.0f}%**, terminal growth "
      f"**{va['terminal_growth_pct']:.0f}%**. Forecast FCF ($bn): "
      + ", ".join(f"{x:.1f}" for x in v["dcf"]["forecast_fcf_usd_bn"]) + ". "
      f"Enterprise value **{_bn(v['dcf']['enterprise_value_usd_bn'])}**, equity value "
      f"**{_bn(v['dcf']['equity_value_usd_bn'])}**, value per share "
      f"**${_num(v['dcf']['value_per_share_usd'])}**.\n")
    a("### Sensitivity — value per share ($) by discount rate (rows) and terminal growth (columns)\n")
    a("| Discount \\ Terminal | 2% | 3% | 4% |\n|---|---|---|---|\n")
    for disc in (9, 10, 11):
        cells = " | ".join(f"${v['sensitivity_per_share_usd'][f'disc_{disc}_term_{t}']:.2f}" for t in (2, 3, 4))
        a(f"| {disc}% | {cells} |\n")
    a(f"\nSensitivity range: **${v['sensitivity_range_usd'][0]:.2f} - ${v['sensitivity_range_usd'][1]:.2f}** per share.\n")
    a("### FCF-growth scenarios (base discount 10%, terminal growth 3%)\n")
    a("| FCF growth | Value per share |\n|---|---|\n")
    for k, val in v["growth_scenarios_per_share_usd"].items():
        a(f"| {k.replace('fcf_growth_', '').replace('pct', '%')} | ${val:.2f} |\n")
    a("\n### Multiples (FY2026, price as above)\n")
    a(f"- P/E: **{_num(m['pe_fy2026'], 1)}x** (EPS diluted ${_num(rows[-1]['eps_diluted'])})\n"
      f"- EV/EBITDA: **{_num(m['ev_to_ebitda_fy2026'], 1)}x** (EBITDA {_bn(m['ebitda_fy2026_usd_bn'])})\n"
      f"- EV/FCF: **{_num(m['ev_to_fcf_fy2026'], 1)}x**\n"
      f"- Market cap: **{_bn(m['market_cap_usd_bn'])}** on {_num(m['shares_outstanding_bn'])}bn shares outstanding\n")
    a("## 5. Risks and Bear Case\n")
    for r in rk["risks"]:
        a(f"- **{r['risk']}** ({r['severity']}): {r['evidence']}\n")
    b = rk["bear_case"]
    a(f"\n**Bear Case:** {b['assumptions']}. Value per share "
      f"**${_num(b['value_per_share_usd'])}**"
      + (f", {_num(b['downside_vs_price_pct'], 0)}% vs the market price. " if b["downside_vs_price_pct"] is not None else ". ")
      + b["story"] + "\n")
    a("## 6. Final investment judgement (Investment Analyst)\n")
    a(an["final_judgement"] + "\n")
    for s in an["what_the_business_does_well"]:
        a(f"- Does well: {s}\n")
    for s in an["what_would_change_the_judgement"]:
        a(f"- Would change the judgement: {s}\n")
    a("\n## Limitations\n")
    a("- The DCF is highly sensitive to its assumptions: the sensitivity table spans "
      f"${v['sensitivity_range_usd'][0]:.2f}-${v['sensitivity_range_usd'][1]:.2f} per share, and the "
      "growth scenarios move it further. Treat the base case as one scenario, not a price target.\n"
      "- Market price is a single as-of snapshot (see date above); multiples move with the price.\n"
      "- No segment split, market-size estimate or peer comparison is included, because "
      "those numbers were not in the sources pulled — they were not invented.\n"
      "- The agents are deterministic rules over filing data, not an LLM: they cannot read "
      "management commentary, 10-K risk-factor text, or news.\n"
      "- Fiscal years end in January; 'FY2026' means the year ended 2026-01-25.\n")
    a("\n*" + an["disclaimer"] + "*\n")
    return "\n".join(lines)


def main():
    os.makedirs(RESULTS, exist_ok=True)
    print("Running Orchestrator...")
    result = orchestrator.run_all()

    with open(os.path.join(RESULTS, "results.json"), "w") as fh:
        json.dump(result, fh, indent=2, default=str)

    report = build_report(result)
    with open(os.path.join(RESULTS, "report.md"), "w") as fh:
        fh.write(report)
    with open(os.path.join(ROOT, "REPORT.md"), "w") as fh:
        fh.write(report)
    html = ("<html><head><meta charset='utf-8'><title>NVIDIA Agent-Team Financial Report</title></head>"
            "<body style='font-family:sans-serif;max-width:900px;margin:2em auto;line-height:1.6'>"
            + "<pre style='white-space:pre-wrap;font-family:inherit'>" + report + "</pre></body></html>")
    with open(os.path.join(RESULTS, "report.html"), "w") as fh:
        fh.write(html)

    charts.revenue_margin_chart(result["fundamental"]["by_year"],
                                os.path.join(RESULTS, "revenue_margin.png"))
    v = result["valuation"]
    charts.valuation_chart(v["dcf"]["value_per_share_usd"],
                           v["sensitivity_range_usd"][0], v["sensitivity_range_usd"][1],
                           result["risk"]["bear_case"]["value_per_share_usd"],
                           result["financial_data"]["price"]["price_usd"],
                           os.path.join(RESULTS, "valuation_range.png"))

    h = result["investment_analyst"]["headline"]
    print(f"Done. Revenue FY2026 ${h['revenue_fy2026_usd_bn']:.1f}bn, "
          f"DCF base ${h['dcf_base_per_share_usd']:.2f}/share, "
          f"price ${h['price_usd']:.2f} as of {h['price_as_of']}.")
    print("See results/results.json, results/report.md, REPORT.md")


if __name__ == "__main__":
    main()
