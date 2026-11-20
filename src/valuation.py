"""Valuation Agent — DCF, P/E, EV/EBITDA (and EV/FCF).

Assumptions are stated, not hidden. This is an educational exercise, not
investment advice. Base case (transparent, chosen before seeing the answer):
  - Base free cash flow = FY2026 FCF (operating cash flow minus capex).
  - 5-year explicit forecast: FCF grows 12% a year.
  - Discount rate (WACC proxy): 10%. Terminal growth: 3%.
  - Shares: shares outstanding at FY2026 year-end.
  - Net cash added to enterprise value; debt subtracted.
Sensitivity tables vary the discount rate, terminal growth and FCF growth
so the reader can see how fragile the answer is.
"""
import math


def _dcf(fcf0, growth, discount, terminal_growth, years=5):
    pv = 0.0
    fcfs = []
    for t in range(1, years + 1):
        f = fcf0 * (1 + growth) ** t
        fcfs.append(f)
        pv += f / (1 + discount) ** t
    tv = fcfs[-1] * (1 + terminal_growth) / (discount - terminal_growth)
    pv += tv / (1 + discount) ** years
    return pv, fcfs, tv


def run(data, fundamental):
    rows = {r["fiscal_year"]: r for r in data["annual_table"]}
    latest = rows[2026]
    fcf = latest["operating_cash_flow"] - latest["capex"]  # FY2026 FCF, USD
    shares = latest["shares_outstanding"]
    eps = latest["eps_diluted"]
    price = data["price"]["price_usd"]

    debt = (latest["long_term_debt"] or 0) + (latest["current_debt"] or 0)
    cash_like = (latest["cash"] or 0) + (latest["marketable_securities"] or 0)
    net_cash = cash_like - debt

    base_growth, base_disc, base_term = 0.12, 0.10, 0.03
    ev, fcfs, tv = _dcf(fcf, base_growth, base_disc, base_term)
    equity = ev + net_cash
    per_share = equity / shares

    # Sensitivity: discount rate x terminal growth (base FCF growth 12%).
    sens = {}
    for disc in (0.09, 0.10, 0.11):
        for term in (0.02, 0.03, 0.04):
            ev_s, _, _ = _dcf(fcf, base_growth, disc, term)
            sens[f"disc_{int(disc*100)}_term_{int(term*100)}"] = round(
                (ev_s + net_cash) / shares, 2)
    sens_values = list(sens.values())

    # Scenarios: FCF growth 8% / 12% / 16% at base discount + terminal growth.
    scenarios = {}
    for g in (0.08, 0.12, 0.16):
        ev_s, _, _ = _dcf(fcf, g, base_disc, base_term)
        scenarios[f"fcf_growth_{int(g*100)}pct"] = round((ev_s + net_cash) / shares, 2)

    # Multiples (only if a real market price was fetched).
    market_cap = price * shares if price else None
    ebitda = latest["operating_income"] + (latest["depreciation_amortisation"] or 0)
    ev_market = (market_cap + debt - cash_like) if market_cap else None
    multiples = {
        "price_usd": price,
        "price_as_of": data["price"].get("as_of"),
        "shares_outstanding_bn": shares / 1e9,
        "market_cap_usd_bn": market_cap / 1e9 if market_cap else None,
        "pe_fy2026": price / eps if price and eps else None,
        "ev_usd_bn": ev_market / 1e9 if ev_market else None,
        "ev_to_ebitda_fy2026": ev_market / ebitda if ev_market and ebitda else None,
        "ev_to_fcf_fy2026": ev_market / fcf if ev_market else None,
        "ebitda_fy2026_usd_bn": ebitda / 1e9,
    }
    return {
        "agent": "Valuation Agent",
        "fcf_fy2026_usd_bn": fcf / 1e9,
        "assumptions": {
            "fcf_base": "FY2026 free cash flow (operating cash flow minus capex)",
            "fcf_growth_5y_pct": 12.0, "discount_rate_pct": 10.0,
            "terminal_growth_pct": 3.0, "forecast_years": 5,
            "shares": "shares outstanding at FY2026 year-end",
            "net_cash_usd_bn": net_cash / 1e9,
        },
        "dcf": {
            "enterprise_value_usd_bn": ev / 1e9,
            "equity_value_usd_bn": equity / 1e9,
            "value_per_share_usd": per_share,
            "forecast_fcf_usd_bn": [round(x / 1e9, 2) for x in fcfs],
            "terminal_value_usd_bn": tv / 1e9,
        },
        "sensitivity_per_share_usd": sens,
        "sensitivity_range_usd": [min(sens_values), max(sens_values)],
        "growth_scenarios_per_share_usd": scenarios,
        "multiples": multiples,
    }
