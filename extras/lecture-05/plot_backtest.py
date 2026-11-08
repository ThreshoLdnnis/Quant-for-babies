"""Export five labelled SIMULATED teaching figures from lecture 05 chart_data.json."""
from __future__ import annotations
import argparse
from datetime import datetime
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

STRATEGIES = ["mom20", "vol20", "turn20", "multi", "reference"]
COLORS = {"mom20": "#ad7e39", "vol20": "#78649c", "turn20": "#7c9a42", "multi": "#087e83", "reference": "#8799a4"}
LABELS = {"mom20": "MOM20 Top3", "vol20": "VOL20 Top3", "turn20": "TURN20 Top3", "multi": "Static multi Top3", "reference": "Equalweight reference (8 stocks)"}
INK, MUTED = "#193346", "#526a79"


def load_data(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("data_kind") != "SIMULATION_ONLY_NOT_REAL_A_SHARE_RESULTS":
        raise ValueError("Only explicitly SIMULATED lecture 05 outputs are accepted")
    if data["strategies"] != STRATEGIES or data["config"]["top_n"] != 3:
        raise ValueError("Unexpected strategy protocol")
    for strategy in STRATEGIES:
        rows = [r for r in data["nav_series"] if r["strategy"] == strategy and r["scenario"] == "base"]
        if len(rows) != 80 or any(not np.isfinite([r["nav"], r["daily_return"], r["drawdown"]]).all() for r in rows):
            raise ValueError("Incomplete NAV series")
        nav = np.asarray([1.] + [r["nav"] for r in rows])
        expected = nav / np.maximum.accumulate(nav) - 1
        if not np.allclose(expected[1:], [r["drawdown"] for r in rows], atol=1e-9):
            raise ValueError("Drawdown differs from NAV including initial value")
    return data


def prepare_output(output: Path) -> Path:
    output = output.resolve()
    marker = output / ".quant_babies_lecture05_figures"
    if output.exists() and (not output.is_dir() or (any(output.iterdir()) and not marker.is_file())):
        raise FileExistsError(f"Refusing non-plot directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    marker.write_text("SIMULATED lecture 05 figures only.\n", encoding="utf-8")
    return output


def score_ranking(data):
    rows = sorted(data["ranking_snapshot"], key=lambda r: r["rank"])
    fig, ax = plt.subplots(figsize=(10.5, 5.3))
    bars = ax.barh([r["symbol"] for r in rows][::-1], [r["score"] for r in rows][::-1],
                   color=["#087e83" if r["selected"] else "#b7c8c5" for r in rows][::-1])
    ax.axvline(0, color="#91a6a7", linewidth=.9)
    ax.set_xlabel("Static mean of three fixed oriented Z-scores")
    ax.set_title(f"SIMULATED score ranking | {rows[0]['signal_date']} close | {len(rows)} eligible stocks", weight="bold", color=INK)
    ax.grid(axis="x", alpha=.16)
    fig.text(.5, .025, "Teal = frozen Top3 targets. Ranking uses current factors only; it is not a filled order or a return prediction guarantee.", ha="center", fontsize=9, color=MUTED)
    fig.tight_layout(rect=(0, .09, 1, 1))
    return fig


def portfolio_weights(data):
    rows = data["weight_snapshot"]
    x = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(12.3, 5.1))
    for offset, field, label, color in [(-.25, "before_weight", "Before trade (opening marks)", "#c0cdcc"),
                                      (0, "target_weight", "Frozen target", "#ad7e39"),
                                      (.25, "after_weight", "Actual after opening fills", "#087e83")]:
        ax.bar(x+offset, [r[field]*100 for r in rows], width=.24, label=label, color=color)
    ax.set_xticks(x, [r["symbol"] for r in rows], rotation=25)
    ax.set_ylabel("Portfolio weight (%)")
    ax.set_title(f"SIMULATED multi/base weights | {rows[0]['trade_date']} opening", weight="bold", color=INK)
    ax.legend(fontsize=8.5, ncol=3, loc="upper right")
    ax.set_ylim(0, 79)
    ax.grid(axis="y", alpha=.17)
    fig.text(.5, .02, "Unfilled/blocked orders, integer lots, available cash and fees make realized holdings differ from targets. CASH remains part of the portfolio.", ha="center", fontsize=9, color=MUTED)
    fig.tight_layout(rect=(0, .08, 1, 1))
    return fig


def base_rows(data, strategy):
    return [r for r in data["nav_series"] if r["strategy"] == strategy and r["scenario"] == "base"]


def nav_comparison(data):
    fig, ax = plt.subplots(figsize=(11.5, 6.0))
    for strategy in STRATEGIES:
        rows = base_rows(data, strategy)
        ax.plot([datetime.fromisoformat(r["trade_date"]) for r in rows], [r["nav"] for r in rows],
                label=LABELS[strategy], color=COLORS[strategy], linewidth=2.3 if strategy == "multi" else 1.5)
    ax.set_ylabel("Net NAV (initial cash = 1)")
    ax.set_title(f"SIMULATED single/multi/reference NAV | {data['start_date']} to {data['end_date']}", weight="bold", color=INK)
    ax.legend(fontsize=8.5, loc="upper left")
    ax.grid(axis="y", alpha=.18)
    locator = mdates.AutoDateLocator(minticks=5, maxticks=8)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    fig.text(.5, .035, "Same 80-date grid, starting cash, signal dates and execution rules; fictional base costs. No actual A-share index is shown.", ha="center", fontsize=9, color=MUTED)
    fig.text(.5, .008, "Cash warmup is included. Three executions on artificial paths cannot establish factor validity or out-of-sample performance.", ha="center", fontsize=9, color=MUTED)
    fig.tight_layout(rect=(0, .1, 1, 1))
    return fig


def drawdown_figure(data):
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    for strategy in ["multi", "reference"]:
        rows = base_rows(data, strategy)
        dates = [datetime.fromisoformat(r["trade_date"]) for r in rows]
        values = [100*r["drawdown"] for r in rows]
        ax.plot(dates, values, label=LABELS[strategy], color=COLORS[strategy], linewidth=1.9)
        if strategy == "multi":
            ax.fill_between(dates, values, 0, color=COLORS[strategy], alpha=.1)
    ax.axhline(0, color="#9cb0af", linewidth=.8)
    ax.set_ylabel("Drawdown from prior running peak (%)")
    ax.set_title("SIMULATED base-cost drawdowns | running peak includes initial NAV = 1", weight="bold", color=INK)
    ax.legend(fontsize=9, loc="lower left")
    ax.grid(axis="y", alpha=.17)
    locator = mdates.AutoDateLocator(minticks=5, maxticks=8)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    fig.text(.5, .018, "MDD is the most negative ratio NAV/running_peak - 1. It is an observed historical path statistic, not a maximum possible future loss.", ha="center", fontsize=9, color=MUTED)
    fig.tight_layout(rect=(0, .08, 1, 1))
    return fig


def cost_sensitivity(data):
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.9))
    colors = {"zero": "#91afaa", "base": "#087e83", "high": "#ad7e39"}
    for scenario in ["zero", "base", "high"]:
        rows = [r for r in data["nav_series"] if r["strategy"] == "multi" and r["scenario"] == scenario]
        axes[0].plot([datetime.fromisoformat(r["trade_date"]) for r in rows], [r["nav"] for r in rows], label=scenario, color=colors[scenario])
    locator = mdates.AutoDateLocator(minticks=3, maxticks=5)
    axes[0].xaxis.set_major_locator(locator)
    axes[0].xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    axes[0].set_ylabel("NAV (initial = 1)")
    axes[0].legend(fontsize=9)
    scenarios = data["cost_sensitivity"]
    axes[1].bar([r["scenario"] for r in scenarios], [100*r["total_return"] for r in scenarios], color=[colors[r["scenario"]] for r in scenarios])
    for i, row in enumerate(scenarios):
        axes[1].text(i, row["total_return"]*100+.1, f"{row['total_return']*100:.2f}%", ha="center", color=INK)
    axes[1].set_ylabel("Whole-sample cumulative return (%)")
    axes[1].set_ylim(0, max(r["total_return"]*100 for r in scenarios)*1.17)
    for ax in axes:
        ax.grid(axis="y", alpha=.17)
    fig.suptitle("SIMULATED static multi cost sensitivity | zero / fictional base / double rates", weight="bold", color=INK)
    fig.text(.5, .02, "Each scenario reruns the entire share/cash ledger. Costs may change affordable lot quantities; the difference is not simply cumulative fees.", ha="center", fontsize=9, color=MUTED)
    fig.tight_layout(rect=(0, .09, 1, .94))
    return fig


def run(input_path: Path, output: Path) -> dict:
    data = load_data(input_path)
    output = prepare_output(output)
    files = []
    with plt.rc_context({"font.family": "DejaVu Sans", "svg.hashsalt": "quant-babies-lecture05",
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK}):
        for name, maker in [("score_ranking", score_ranking), ("portfolio_weights", portfolio_weights),
                            ("nav_comparison", nav_comparison), ("drawdown", drawdown_figure),
                            ("cost_sensitivity", cost_sensitivity)]:
            fig = maker(data)
            for extension in ["png", "svg"]:
                path = output / f"{name}.{extension}"
                metadata = {"Date": None} if extension == "svg" else {"Software": "Quant for Babies / matplotlib"}
                fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white", metadata=metadata)
                files.append(path.name)
            plt.close(fig)
    return {"data_kind": data["data_kind"], "files": files}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = run(args.input, args.output)
    except (OSError, ValueError, KeyError) as exc:
        print(f"Figure export failed: {exc}", file=__import__("sys").stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
