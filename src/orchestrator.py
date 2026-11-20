"""Orchestrator Agent — allocate tasks, coordinate, check results, integrate.

Runs the agents in dependency order, checks each one's output before passing
it on, and collects everything into one result dict for the report.
"""
import financial_data
import fundamental
import industry
import valuation
import risk
import investment_analyst


def _check(name, output, required):
    missing = [k for k in required if k not in output or output[k] is None]
    if missing:
        raise ValueError(f"{name} output missing: {missing}")
    return output


def run_all():
    data = _check("Financial Data Agent", financial_data.run(),
                  ["annual_table", "price", "sources"])
    fund = _check("Fundamental Agent", fundamental.run(data),
                  ["by_year", "leverage"])
    ind = _check("Industry Agent", industry.run(data, fund),
                 ["conclusion", "moat_assessment"])
    val = _check("Valuation Agent", valuation.run(data, fund),
                 ["dcf", "sensitivity_per_share_usd", "multiples"])
    rsk = _check("Risk Agent", risk.run(data, fund, val),
                 ["risks", "bear_case"])
    ana = _check("Investment Analyst",
                 investment_analyst.run(data, fund, ind, val, rsk),
                 ["final_judgement", "headline"])
    return {"financial_data": data, "fundamental": fund, "industry": ind,
            "valuation": val, "risk": rsk, "investment_analyst": ana}
