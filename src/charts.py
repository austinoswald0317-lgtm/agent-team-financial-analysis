"""Charts for the report (matplotlib, Agg backend — no display needed)."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def revenue_margin_chart(by_year, out_path):
    years = sorted(by_year)
    rev = [by_year[y]["revenue_usd_bn"] for y in years]
    gm = [by_year[y]["gross_margin_pct"] for y in years]
    nm = [by_year[y]["net_margin_pct"] for y in years]
    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    ax1.bar([str(y) for y in years], rev, color="#76b900")
    ax1.set_ylabel("Revenue ($bn)")
    ax1.set_title("NVIDIA — revenue and margins, FY2022-FY2026")
    for i, v in enumerate(rev):
        ax1.text(i, v + 4, f"{v:.0f}", ha="center", fontsize=9)
    ax2 = ax1.twinx()
    ax2.plot([str(y) for y in years], gm, marker="o", label="Gross margin %")
    ax2.plot([str(y) for y in years], nm, marker="s", label="Net margin %")
    ax2.set_ylabel("Margin (%)")
    ax2.set_ylim(0, 100)
    ax2.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def valuation_chart(dcf_base, sens_lo, sens_hi, bear, price, out_path):
    # DCF range is a bar; DCF base and Bear Case are single values, so they
    # are markers, not bars (a bar would falsely imply a range).
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.barh(2, sens_hi - sens_lo, left=sens_lo, height=0.45, color="#76b900")
    ax.text(sens_hi + 2, 2, f"${sens_hi:.0f}", va="center", fontsize=10)
    ax.text(sens_lo - 2, 2, f"${sens_lo:.0f}", va="center", ha="right", fontsize=10)
    ax.plot([dcf_base], [1], marker="D", markersize=9, color="#1f77b4")
    ax.text(dcf_base + 2, 1, f"DCF base ${dcf_base:.2f}", va="center", fontsize=10)
    ax.plot([bear], [0], marker="v", markersize=9, color="#888888")
    ax.text(bear + 2, 0, f"Bear Case ${bear:.2f}", va="center", fontsize=10)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(["Bear Case", "DCF base", "DCF range"])
    ax.set_xlabel("Value per share ($)")
    ax.set_title("Valuation range vs market price")
    if price:
        ax.axvline(price, color="red", linestyle="--", label=f"Market price ${price:.2f}")
        ax.legend(fontsize=9)
    ax.set_xlim(0, max(sens_hi, price or 0) * 1.15)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
