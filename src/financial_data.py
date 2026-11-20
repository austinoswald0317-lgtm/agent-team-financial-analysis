"""Financial Data Agent — reads real filings and market data.

Role (per Austin's diagram): read 10-K / 10-Q and financial data.
Output: standardised financial data.

Sources (no API key needed):
- SEC EDGAR company-facts API:
  https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json
  (NVIDIA CORP, CIK 1045810; latest FY2026 10-K filed 2026-02-25,
  accession 0001045810-26-000021)
- Nasdaq quote API for the market price (as-of date recorded):
  https://api.nasdaq.com/api/quote/NVDA/info?assetclass=stocks

No numbers are invented. If a tag is missing from the XBRL facts, the
agent records it as missing instead of guessing a value.
"""
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")

CIK = "0001045810"
COMPANY = "NVIDIA CORP"
TICKER = "NVDA"
FACTS_URL = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json"
PRICE_URL = "https://api.nasdaq.com/api/quote/NVDA/info?assetclass=stocks"
HEADERS = {"User-Agent": "Austin research austin@example.com",
           "Accept": "application/json"}

# us-gaap tags we use, with a short label for the standardised table.
TAGS = {
    "revenue": "Revenues",
    "gross_profit": "GrossProfit",
    "operating_income": "OperatingIncomeLoss",
    "net_income": "NetIncomeLoss",
    "rd_expense": "ResearchAndDevelopmentExpense",
    "operating_cash_flow": "NetCashProvidedByUsedInOperatingActivities",
    "capex": "PaymentsToAcquireProductiveAssets",
    "cash": "CashAndCashEquivalentsAtCarryingValue",
    "marketable_securities": "AvailableForSaleSecuritiesDebtSecurities",
    "long_term_debt": "LongTermDebt",
    "current_debt": "LongTermDebtCurrent",
    "total_assets": "Assets",
    "current_assets": "AssetsCurrent",
    "total_liabilities": "Liabilities",
    "current_liabilities": "LiabilitiesCurrent",
    "equity": "StockholdersEquity",
    "depreciation_amortisation": "DepreciationDepletionAndAmortization",
    "diluted_shares": "WeightedAverageNumberOfDilutedSharesOutstanding",
    "shares_outstanding": "CommonStockSharesOutstanding",
    "eps_diluted": "EarningsPerShareDiluted",
}


def _get_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or HEADERS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fiscal_year(end_date):
    """NVIDIA's fiscal year ends in January: year ending Jan 2026 = FY2026."""
    y, m, _d = (int(p) for p in end_date.split("-"))
    return y if m > 1 else y


def _annual_series(facts, tag):
    """Annual 10-K values for one tag, deduped by period end (latest filing wins)."""
    if tag not in facts["facts"]["us-gaap"]:
        return {}, None
    best = {}
    for unit, rows in facts["facts"]["us-gaap"][tag]["units"].items():
        for r in rows:
            if r.get("form") != "10-K" or r.get("fp") != "FY":
                continue
            end = r["end"]
            if end not in best or r.get("filed", "") >= best[end].get("filed", ""):
                best[end] = r
    out = {}
    for end, r in best.items():
        out[fiscal_year(end)] = {"value": r["val"], "end": end,
                                 "filed": r.get("filed"), "accn": r.get("accn")}
    return out, None


def fetch_price():
    """Latest Nasdaq last-sale price. Returns dict or None (never invented)."""
    try:
        data = _get_json(PRICE_URL, headers={"User-Agent": "Mozilla/5.0",
                                              "Accept": "application/json"})
        primary = data["data"]["primaryData"]
        price = float(primary["lastSalePrice"].replace("$", "").replace(",", ""))
        return {"price_usd": price,
                "as_of": primary.get("lastTradeTimestamp"),
                "source": PRICE_URL}
    except Exception as exc:  # market data is optional; SEC data is the core
        return {"price_usd": None, "as_of": None, "source": PRICE_URL,
                "error": str(exc)}


def run():
    """Fetch, standardise and save. Returns the agent's structured output."""
    facts = _get_json(FACTS_URL)
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, "companyfacts_nvda.json"), "w") as fh:
        json.dump(facts, fh)

    series = {}
    for key, tag in TAGS.items():
        series[key], _ = _annual_series(facts, tag)

    # Keep five fiscal years, FY2022-FY2026 (ends Jan 2022 - Jan 2026).
    years = [2022, 2023, 2024, 2025, 2026]
    table = []
    for fy in years:
        row = {"fiscal_year": fy}
        for key in TAGS:
            row[key] = series.get(key, {}).get(fy, {}).get("value")
        row["period_end"] = series.get("revenue", {}).get(fy, {}).get("end")
        row["filed"] = series.get("revenue", {}).get(fy, {}).get("filed")
        row["accession"] = series.get("revenue", {}).get(fy, {}).get("accn")
        table.append(row)

    # Latest reported quarter: the most recently filed 10-Q. XBRL 10-Q rows
    # come in two flavours for the same period end — cumulative year-to-date
    # (start in January, the fiscal-year start) and standalone quarter
    # (start = quarter start). Use the cumulative row for the headline and
    # the standalone row for the single-quarter figure.
    def _q(tag, cumulative):
        rows = [r for r in facts["facts"]["us-gaap"].get(tag, {}).get("units", {}).get("USD", [])
                if r.get("form") == "10-Q" and r.get("start")]
        rows = [r for r in rows
                if (r["start"].split("-")[1] == "01") == cumulative]
        if not rows:
            return None
        return max(rows, key=lambda r: (r.get("filed", ""), r.get("end", "")))

    cum_rev = _q("Revenues", True)
    cum_ni = _q("NetIncomeLoss", True)
    st_rev = _q("Revenues", False)
    st_ni = _q("NetIncomeLoss", False)
    # Standalone row must match the cumulative row's period end.
    if st_rev and cum_rev and st_rev["end"] != cum_rev["end"]:
        st_rev = None
    if st_ni and cum_ni and st_ni["end"] != cum_ni["end"]:
        st_ni = None
    end = cum_rev["end"] if cum_rev else None
    fy_q = (int(end.split("-")[0]) + 1) if end and int(end.split("-")[1]) >= 2 else None
    latest_quarter = {
        "period": (f"{cum_rev.get('fp')} FY{fy_q} ended {end} (cumulative year-to-date)"
                   if cum_rev else None),
        "revenue_usd": cum_rev["val"] if cum_rev else None,
        "net_income_usd": cum_ni["val"] if cum_ni else None,
        "filed": cum_rev.get("filed") if cum_rev else None,
        "standalone_revenue_usd": st_rev["val"] if st_rev else None,
        "standalone_net_income_usd": st_ni["val"] if st_ni else None,
        "note": "10-Q headline figures are cumulative year-to-date; the standalone figure is the single quarter.",
    }

    price = fetch_price()

    # Standardised CSV (small, committed to the repo).
    import csv
    with open(os.path.join(DATA_DIR, "standardised_financials.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["fiscal_year", "period_end", "filed",
                                           "accession"] + list(TAGS))
        w.writeheader()
        for row in table:
            w.writerow(row)

    return {
        "agent": "Financial Data Agent",
        "company": COMPANY, "ticker": TICKER, "cik": CIK,
        "sources": {"sec_companyfacts": FACTS_URL, "nasdaq_price": PRICE_URL},
        "annual_table": table,
        "latest_quarter": latest_quarter,
        "price": price,
        "missing_tags": [k for k, v in TAGS.items()
                         if k not in facts["facts"]["us-gaap"]],
        "notes": [
            "Fiscal year ends in January: FY2026 ended 2026-01-25, 10-K filed 2026-02-25.",
            "Marketable securities use AvailableForSaleSecuritiesDebtSecurities; "
            "MarketableSecuritiesCurrent has no FY2026 value in the company-facts file.",
            "CapEx uses PaymentsToAcquireProductiveAssets (the tag NVIDIA reports); "
            "PaymentsToAcquirePropertyPlantAndEquipment has no recent values.",
            "Segment revenue split is not present in the company-facts file, so the "
            "Industry Agent does not invent one (see industry.py).",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
