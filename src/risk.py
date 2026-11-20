"""Risk Agent — identify risks and build a Bear Case.

Risks are tied to numbers in the filings where possible; where a risk is
qualitative (export controls, customer concentration), it is labelled as
such and not given a made-up probability or dollar figure.
"""
import math


def run(data, fundamental, valuation):
    rows = {r["fiscal_year"]: r for r in data["annual_table"]}
    by_year = fundamental["by_year"]
    price = data["price"]["price_usd"]
    dcf_base = valuation["dcf"]["value_per_share_usd"]

    risks = [
        {
            "risk": "Valuation risk — the price already assumes a lot of growth",
            "evidence": (
                f"At ${price:.2f} (as of {data['price'].get('as_of')}), the share price is "
                f"{(price / dcf_base - 1) * 100:.0f}% above this project's DCF base case "
                f"(${dcf_base:.2f}). The DCF only reaches the current price if FCF grows "
                "well above 12% a year or the discount rate is well below 10%."
                if price else "No market price was fetched, so the price-vs-DCF gap could not be measured."
            ),
            "severity": "high",
        },
        {
            "risk": "Demand cyclicality — the AI wave can pause, as it did in FY2023",
            "evidence": (
                f"Revenue growth was {by_year[2023]['revenue_growth_pct']:.1f}% in FY2023 "
                f"and operating cash flow fell from ${rows[2022]['operating_cash_flow']/1e9:.1f}bn "
                f"(FY2022) to ${rows[2023]['operating_cash_flow']/1e9:.1f}bn (FY2023). "
                "A pause in data-centre spending would hit revenue, margins and FCF at once."
            ),
            "severity": "high",
        },
        {
            "risk": "Customer concentration",
            "evidence": (
                "A few hyperscale customers buy most data-centre GPUs. The exact share "
                "is not in the XBRL facts pulled here, so it is flagged qualitatively, "
                "not quantified. Losing or delaying one large customer matters."
            ),
            "severity": "medium",
        },
        {
            "risk": "Competition and custom silicon",
            "evidence": (
                "AMD competes directly, and large cloud customers design their own AI "
                "chips. No peer financials were pulled, so this is a qualitative risk; "
                "the defence is R&D spend, which rose to "
                f"${rows[2026]['rd_expense']/1e9:.1f}bn in FY2026."
            ),
            "severity": "medium",
        },
        {
            "risk": "Export controls and geopolitics (qualitative)",
            "evidence": (
                "US export controls on advanced chips to China are a known, recurring "
                "risk for NVIDIA. This project does not estimate the revenue at stake."
            ),
            "severity": "medium",
        },
        {
            "risk": "Dilution / share-based compensation",
            "evidence": (
                f"Shares outstanding fell from {rows[2024]['shares_outstanding']/1e9:.2f}bn "
                f"(FY2024) to {rows[2026]['shares_outstanding']/1e9:.2f}bn (FY2026) — "
                "buybacks more than offset dilution over this window, but that depends "
                "on buybacks continuing."
            ),
            "severity": "low",
        },
    ]

    # Bear Case: FCF growth 8% (not 12%), discount 11%, terminal growth 2%.
    from valuation import _dcf
    fcf = rows[2026]["operating_cash_flow"] - rows[2026]["capex"]
    debt = (rows[2026]["long_term_debt"] or 0) + (rows[2026]["current_debt"] or 0)
    cash_like = (rows[2026]["cash"] or 0) + (rows[2026]["marketable_securities"] or 0)
    ev_bear, _, _ = _dcf(fcf, 0.08, 0.11, 0.02)
    bear_ps = (ev_bear + cash_like - debt) / rows[2026]["shares_outstanding"]
    bear_case = {
        "assumptions": "FCF growth 8% (vs 12% base), discount rate 11% (vs 10%), terminal growth 2% (vs 3%)",
        "value_per_share_usd": bear_ps,
        "downside_vs_price_pct": ((bear_ps / price - 1) * 100) if price else None,
        "story": (
            "AI data-centre spending pauses for a year, growth slows, and investors "
            "demand a higher return for the risk. FCF still grows, but the price paid "
            "today would be well above even a cautious fair value."
        ),
    }
    return {"agent": "Risk Agent", "risks": risks, "bear_case": bear_case}
