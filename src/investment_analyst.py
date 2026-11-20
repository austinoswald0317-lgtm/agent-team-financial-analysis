"""Investment Analyst — integrate all agents into a final judgement.

The judgement is an educational exercise, not investment advice and not a
recommendation to buy or sell. It states what the business does well, what
the price assumes, and where the DCF sits relative to the price.
"""


def run(data, fundamental, industry, valuation, risk):
    price = data["price"]["price_usd"]
    dcf = valuation["dcf"]["value_per_share_usd"]
    lo, hi = valuation["sensitivity_range_usd"]
    by_year = fundamental["by_year"]
    latest = by_year[2026]

    # FCF growth rate (5 years, 10% discount, 3% terminal) at which the DCF
    # would equal the current price — found by bisection, not assumed.
    threshold_growth = None
    if price:
        from valuation import _dcf as _dcf_fn
        fcf0 = data["annual_table"][-1]["operating_cash_flow"] - data["annual_table"][-1]["capex"]
        lev = fundamental["leverage"]
        net_cash = lev["net_cash_usd_bn"] * 1e9
        shares = data["annual_table"][-1]["shares_outstanding"]
        blo, bhi = 0.0, 0.60
        for _ in range(50):
            mid = (blo + bhi) / 2
            ev, _, _ = _dcf_fn(fcf0, mid, 0.10, 0.03)
            if (ev + net_cash) / shares < price:
                blo = mid
            else:
                bhi = mid
        threshold_growth = bhi * 100

    if price:
        gap = (price / dcf - 1) * 100
        if price > hi:
            verdict = (
                f"Strong business, demanding price. At ${price:.2f} the market price is "
                f"above even the top of this DCF sensitivity range (${lo:.2f}-${hi:.2f}), "
                f"and {gap:.0f}% above the base case (${dcf:.2f}). The business would have "
                "to grow faster than the 12% FCF growth assumed here — or be discounted "
                "at less than 10% — for the current price to equal the DCF value."
            )
        elif price > dcf:
            verdict = "Strong business, price above the DCF base case but inside the sensitivity range."
        else:
            verdict = "Strong business, price at or below the DCF base case."
    else:
        verdict = "Strong business; no market price was fetched, so no price-vs-value judgement can be made."

    return {
        "agent": "Investment Analyst",
        "final_judgement": verdict,
        "headline": {
            "revenue_fy2026_usd_bn": latest["revenue_usd_bn"],
            "revenue_cagr_fy22_fy26_pct": fundamental["revenue_cagr_fy22_fy26_pct"],
            "gross_margin_fy2026_pct": latest["gross_margin_pct"],
            "net_margin_fy2026_pct": latest["net_margin_pct"],
            "fcf_fy2026_usd_bn": latest["fcf_usd_bn"],
            "dcf_base_per_share_usd": dcf,
            "dcf_sensitivity_range_usd": [lo, hi],
            "price_usd": price,
            "price_as_of": data["price"].get("as_of"),
            "pe_fy2026": valuation["multiples"]["pe_fy2026"],
        },
        "what_the_business_does_well": [
            f"Revenue CAGR {fundamental['revenue_cagr_fy22_fy26_pct']:.0f}% (FY2022-FY2026) with a {latest['gross_margin_pct']:.1f}% gross margin.",
            f"Free cash flow of ${latest['fcf_usd_bn']:.1f}bn in FY2026, a {latest['fcf_margin_pct']:.0f}% FCF margin.",
            f"Net cash of ${fundamental['leverage']['net_cash_usd_bn']:.1f}bn — the balance sheet is not the risk.",
        ],
        "what_would_change_the_judgement": [
            f"FCF growth sustained at about {threshold_growth:.0f}% a year for 5 years (vs 12% in the base "
            "case, at the same 10% discount rate) would be needed for the DCF to reach "
            "the current price — even 16% growth only gives "
            f"${valuation['growth_scenarios_per_share_usd']['fcf_growth_16pct']:.2f} a share."
            if threshold_growth else
            "Sustained FCF growth well above the 12% base case would be needed for the DCF to reach the current price.",
            "A data-centre spending pause (the FY2023 pattern) would cut the DCF sharply — see the Bear Case.",
            "A lower discount rate (e.g. if rates fall) lifts every DCF value in the sensitivity table.",
        ],
        "disclaimer": (
            "Educational exercise only. This is not investment advice, not a "
            "recommendation to buy or sell any security, and the DCF is only as good "
            "as its stated assumptions."
        ),
    }
