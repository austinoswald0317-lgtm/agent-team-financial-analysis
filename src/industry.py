"""Industry Agent — analyse industry and competitiveness.

Input: Financial Data + Fundamental outputs.
Output: an industry / competition analysis.

Honesty rule: this agent does NOT invent market-size figures, market-share
figures, or a segment revenue split. The SEC company-facts file used here
contains no segment split for NVIDIA, and no peer filings were pulled, so
those numbers are recorded as unavailable. The analysis therefore rests on
what the filings do show: growth, margins, R&D intensity, and the shape of
the demand cycle — plus qualitative moat factors that follow from them.
"""
import math


def run(data, fundamental):
    by_year = fundamental["by_year"]
    years = sorted(by_year)
    latest = by_year[years[-1]]

    # R&D in dollars and as a share of revenue; R&D grew every year?
    rows = {r["fiscal_year"]: r for r in data["annual_table"]}
    rd = {fy: rows[fy]["rd_expense"] / 1e9 for fy in years if rows[fy]["rd_expense"]}
    rd_growth = ((rd[years[-1]] / rd[years[0]]) ** (1 / (years[-1] - years[0])) - 1) * 100

    # Demand-cycle evidence from the company's own history.
    growth = {fy: by_year[fy]["revenue_growth_pct"] for fy in years}
    slowest = min((fy for fy in years if growth[fy] is not None),
                  key=lambda fy: growth[fy])

    moat = [
        "Scale + switching costs: data-centre customers build systems, software "
        "(CUDA) and models around NVIDIA's platform; changing supplier means "
        "re-engineering, which is why gross margin stayed above 70% in FY2026.",
        "R&D engine: R&D spend rose from ${:.1f}bn (FY2022) to ${:.1f}bn (FY2026), "
        "a {:.0f}% CAGR — the moat is funded every year, not a one-off patent.".format(
            rd[years[0]], rd[years[-1]], rd_growth),
        "Counterweight: that moat is tied to one demand wave (AI data-centre "
        "spending). FY2023 shows the cycle: revenue growth slowed to {:.1f}% and "
        "operating cash flow fell, before the AI wave lifted FY2024-FY2026.".format(
            growth[slowest]),
    ]
    risks = [
        "Customer concentration risk is real in this industry (a few hyperscalers "
        "buy most data-centre GPUs) — but the exact share is not in the XBRL facts "
        "pulled here, so it is flagged, not quantified.",
        "Competitors (AMD, custom silicon from cloud customers) attack the same "
        "market; no peer financials were pulled in this project, so no "
        "head-to-head margin comparison is claimed.",
    ]
    return {
        "agent": "Industry Agent",
        "rd_usd_bn_by_year": rd,
        "rd_cagr_fy22_fy26_pct": rd_growth,
        "revenue_growth_pct_by_year": growth,
        "slowest_growth_year": slowest,
        "moat_assessment": moat,
        "competitive_risks": risks,
        "not_available": [
            "Segment revenue split (Compute & Networking vs Graphics) — not present "
            "in the SEC company-facts file used here.",
            "Total addressable market size / market share — no independent source "
            "was pulled; not estimated.",
            "Peer financials — no peer filings were pulled in this project.",
        ],
        "conclusion": (
            "A dominant position in a fast-growing but cyclical market: "
            f"revenue CAGR {fundamental['revenue_cagr_fy22_fy26_pct']:.0f}% (FY2022-FY2026), "
            f"gross margin {latest['gross_margin_pct']:.1f}% in FY2026, funded by "
            "R&D that itself compounds. The moat looks real, but it is a "
            "single-wave moat — the FY2023 slowdown is the reminder."
        ),
    }
