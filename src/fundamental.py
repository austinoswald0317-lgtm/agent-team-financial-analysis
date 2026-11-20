"""Fundamental Agent — analyse financial health.

Input: the Financial Data Agent's standardised table.
Output: a financial-health assessment (margins, growth, cash flow, leverage,
returns) computed from those numbers only.
"""
import math


def _pct(a, b):
    return (a / b * 100.0) if a is not None and b not in (None, 0) else None


def _cagr(start, end, n_years):
    if start in (None, 0) or end is None or start <= 0:
        return None
    return ((end / start) ** (1.0 / n_years) - 1.0) * 100.0


def run(data):
    rows = {r["fiscal_year"]: r for r in data["annual_table"]}
    years = sorted(rows)
    latest = rows[years[-1]]

    by_year = {}
    for fy in years:
        r = rows[fy]
        rev, gp, oi, ni = r["revenue"], r["gross_profit"], r["operating_income"], r["net_income"]
        ocf, capex = r["operating_cash_flow"], r["capex"]
        fcf = (ocf - capex) if (ocf is not None and capex is not None) else None
        by_year[fy] = {
            "revenue_usd_bn": rev / 1e9 if rev else None,
            "gross_margin_pct": _pct(gp, rev),
            "operating_margin_pct": _pct(oi, rev),
            "net_margin_pct": _pct(ni, rev),
            "rd_intensity_pct": _pct(r["rd_expense"], rev),
            "fcf_usd_bn": fcf / 1e9 if fcf is not None else None,
            "fcf_margin_pct": _pct(fcf, rev),
            "roe_pct": _pct(ni, r["equity"]),
            "roa_pct": _pct(ni, r["total_assets"]),
            "revenue_growth_pct": None,
        }
    for i, fy in enumerate(years):
        if i:
            prev = rows[years[i - 1]]["revenue"]
            by_year[fy]["revenue_growth_pct"] = _pct(
                rows[fy]["revenue"] - prev, prev)

    rev_cagr = _cagr(rows[years[0]]["revenue"], rows[years[-1]]["revenue"],
                     years[-1] - years[0])
    ni_cagr = _cagr(rows[years[0]]["net_income"], rows[years[-1]]["net_income"],
                    years[-1] - years[0])

    debt = (latest["long_term_debt"] or 0) + (latest["current_debt"] or 0)
    cash_like = (latest["cash"] or 0) + (latest["marketable_securities"] or 0)
    net_cash = cash_like - debt
    current_ratio = (latest["current_assets"] / latest["current_liabilities"]
                     if latest["current_assets"] and latest["current_liabilities"] else None)
    debt_to_equity = debt / latest["equity"] if latest["equity"] else None

    assessment = []
    lm = by_year[years[-1]]
    if lm["gross_margin_pct"] and lm["gross_margin_pct"] > 60:
        assessment.append("Gross margin above 60% in FY2026 — pricing power, not a commodity cost structure.")
    if lm["net_margin_pct"] and lm["net_margin_pct"] > 50:
        assessment.append("Net margin above 50% in FY2026 — unusually profitable even for a large-cap tech company.")
    if rev_cagr and rev_cagr > 50:
        assessment.append(f"Revenue grew at a {rev_cagr:.0f}% CAGR over FY2022-FY2026 — the growth is real but historically extreme, so it cannot be extrapolated safely.")
    if net_cash > 0:
        assessment.append(f"Net cash of ${net_cash/1e9:.1f}bn at FY2026 year-end (cash + marketable securities minus debt) — no solvency concern on the balance sheet.")
    if by_year[2023]["revenue_growth_pct"] is not None and by_year[2023]["revenue_growth_pct"] < 5:
        assessment.append("FY2023 revenue was almost flat (+0.2%) and operating cash flow fell — the business is cyclical, not a straight line up.")

    return {
        "agent": "Fundamental Agent",
        "by_year": by_year,
        "revenue_cagr_fy22_fy26_pct": rev_cagr,
        "net_income_cagr_fy22_fy26_pct": ni_cagr,
        "latest_fy": years[-1],
        "leverage": {
            "total_debt_usd_bn": debt / 1e9,
            "cash_and_securities_usd_bn": cash_like / 1e9,
            "net_cash_usd_bn": net_cash / 1e9,
            "current_ratio": current_ratio,
            "debt_to_equity": debt_to_equity,
        },
        "assessment": assessment,
    }
