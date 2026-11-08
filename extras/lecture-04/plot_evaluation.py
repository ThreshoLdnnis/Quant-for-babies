"""Export SIMULATED lecture 04 method figures from local chart_data.json.

No data collection, strategy return, NAV, or statistical significance claim is made.
"""
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


FACTORS = ["mom20", "vol20", "turn20"]
COLORS = {"mom20": "#087e83", "vol20": "#ad7e39", "turn20": "#7e668d"}
LABELS = {"mom20": "MOM20", "vol20": "VOL20", "turn20": "TURN20"}
INK = "#193346"
MUTED = "#526a79"


def load_data(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("data_kind") != "SIMULATION_ONLY_NOT_REAL_A_SHARE_RESULTS":
        raise ValueError("Only the explicitly SIMULATED lecture 04 export is accepted")
    if data.get("factor_names") != FACTORS or data.get("horizon") != 20:
        raise ValueError("Unexpected factors or horizon")
    if len(data["snapshot"]) != data["snapshot_n"] or data["snapshot_n"] < 5:
        raise ValueError("Unexpected snapshot sample")
    for row in data["snapshot"]:
        if not np.isfinite([row[f"{factor}_score"] for factor in FACTORS] + [row["future_return_20"]]).all():
            raise ValueError("Nonfinite snapshot")
    matrix = np.asarray(data["correlation"]["matrix"], dtype=float)
    values = np.asarray(data["correlation"]["score_values"], dtype=float)
    if matrix.shape != (3, 3) or not np.allclose(matrix, np.corrcoef(values), atol=1e-9, rtol=1e-9):
        raise ValueError("Correlation matrix and common sample differ")
    return data


def prepare_output(output: Path) -> Path:
    output = output.resolve()
    marker = output / ".quant_babies_lecture04_figures"
    if output.exists() and not output.is_dir():
        raise FileExistsError(f"Not a directory: {output}")
    if output.exists() and any(output.iterdir()) and not marker.exists():
        raise FileExistsError(f"Refusing to overwrite a non-plot directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    marker.write_text("SIMULATED lecture 04 figures only.\n", encoding="utf-8")
    return output


def save(figure, folder: Path, name: str) -> list[str]:
    files = []
    for extension in ("png", "svg"):
        path = folder / f"{name}.{extension}"
        metadata = {"Date": None} if extension == "svg" else {"Software": "Quant for Babies / matplotlib"}
        figure.savefig(path, dpi=180, facecolor="white", bbox_inches="tight", metadata=metadata)
        files.append(path.name)
    plt.close(figure)
    return files


def scatter_figure(data: dict):
    figure, axes = plt.subplots(1, 3, figsize=(14.4, 4.8), sharey=True)
    sample = data["snapshot"]
    for axis, factor in zip(axes, FACTORS):
        x = [row[f"{factor}_score"] for row in sample]
        y = [100 * row["future_return_20"] for row in sample]
        axis.axhline(0, color="#b9c9c9", linewidth=.9)
        axis.axvline(0, color="#b9c9c9", linewidth=.9)
        axis.scatter(x, y, s=52, color=COLORS[factor], zorder=3)
        for row, xi, yi in zip(sample, x, y):
            axis.annotate(row["symbol"], (xi, yi), xytext=(4, 5), textcoords="offset points", fontsize=7)
        axis.set_xlabel(f"{LABELS[factor]} fixed oriented Z-score")
        axis.set_title(LABELS[factor], color=INK)
        axis.grid(axis="y", alpha=.18)
        axis.margins(.18)
    axes[0].set_ylabel("Future 20-session price return (%)")
    figure.suptitle(f"SIMULATED factor vs forward label | {data['snapshot_date']} | n={data['snapshot_n']}",
                    color=INK, weight="bold", fontsize=15)
    figure.text(.5, .015, "One small cross-section; labels are known later. These are not executable trading returns or causal evidence.",
                ha="center", fontsize=10, color=MUTED)
    figure.tight_layout(rect=(0, .08, 1, .91))
    return figure


def ic_figure(data: dict):
    figure, axes = plt.subplots(3, 1, figsize=(11.8, 8.4), sharex=True, sharey=True)
    for axis, factor in zip(axes, FACTORS):
        rows = [row for row in data["ic_series"] if row["factor"] == factor]
        dates = [datetime.fromisoformat(row["trade_date"]) for row in rows]
        values = [np.nan if row["rank_ic"] is None else row["rank_ic"] for row in rows]
        n_valid = sum(np.isfinite(values))
        axis.plot(dates, values, color=COLORS[factor], linewidth=1.7, marker="o", markersize=2.8)
        axis.axhline(0, color="#9bb2b5", linewidth=1)
        axis.set_ylim(-1.06, 1.06)
        axis.set_ylabel("Rank IC")
        axis.set_title(f"{LABELS[factor]} | {n_valid} valid daily cross-sections", fontsize=11, loc="left", color=INK)
        axis.grid(axis="y", alpha=.2)
    locator = mdates.AutoDateLocator(minticks=4, maxticks=8)
    axes[-1].xaxis.set_major_locator(locator)
    axes[-1].xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    figure.suptitle("SIMULATED daily Rank IC | fixed 20-session forward labels", fontsize=15, weight="bold", color=INK)
    figure.text(.5, .018, "Daily forward windows overlap. Dates are not independent; no naive t-test or annualized ICIR is reported.",
                ha="center", fontsize=10, color=MUTED)
    figure.tight_layout(rect=(0, .06, 1, .94))
    return figure


def quintile_figure(data: dict):
    figure, axes = plt.subplots(1, 3, figsize=(14.4, 4.9), sharey=True)
    for axis, factor in zip(axes, FACTORS):
        rows = sorted([r for r in data["quintile_mean_common"] if r["factor"] == factor], key=lambda r: r["quintile"])
        groups = [r["quintile"] for r in rows]
        values = [100 * r["mean_forward_return_20"] for r in rows]
        axis.bar(groups, values, color=COLORS[factor], width=.68)
        axis.axhline(0, color="#819b9f", linewidth=1)
        axis.set_xticks([1, 2, 3, 4, 5], ["Q1\nLow", "Q2", "Q3", "Q4", "Q5\nHigh"])
        axis.set_title(f"{LABELS[factor]} | {rows[0]['n_periods']} dates", color=INK)
        axis.set_xlabel("Fixed oriented factor score quintile")
        axis.grid(axis="y", alpha=.17)
    axes[0].set_ylabel("Mean 20-session forward price return (%)")
    figure.suptitle(f"SIMULATED quintile forward returns | {data['common_quintile_n_dates']} common eligible dates", fontsize=15, weight="bold", color=INK)
    figure.text(.5, .015, "Same rule-based date intersection for all factors; overlapping 20-session means, not daily P&L, NAV, or a trading backtest.",
                ha="center", fontsize=10, color=MUTED)
    figure.tight_layout(rect=(0, .08, 1, .91))
    return figure


def correlation_figure(data: dict):
    matrix = np.asarray(data["correlation"]["matrix"], dtype=float)
    figure, axis = plt.subplots(figsize=(7.8, 6.4))
    image = axis.imshow(matrix, vmin=-1, vmax=1, cmap="coolwarm")
    axis.set_xticks(range(3), [LABELS[f] for f in FACTORS])
    axis.set_yticks(range(3), [LABELS[f] for f in FACTORS])
    for i in range(3):
        for j in range(3):
            axis.text(j, i, f"{matrix[i,j]:+.2f}", ha="center", va="center", fontsize=19,
                      color="white" if abs(matrix[i,j]) > .55 else INK)
    figure.colorbar(image, ax=axis, shrink=.8, label="Pearson correlation")
    axis.set_title(f"SIMULATED fixed factor-score correlations\n{data['snapshot_date']} | common n={data['correlation']['n_common']}",
                   color=INK, fontsize=13, weight="bold", pad=18)
    figure.text(.5, .018, "Both axes are current factor scores. This is redundancy analysis, not factor-to-future-return Rank IC.",
                ha="center", fontsize=8.8, color=MUTED)
    figure.tight_layout(rect=(0, .07, 1, 1))
    return figure


def stability_figure(data: dict):
    figure, axes = plt.subplots(1, 2, figsize=(11.6, 4.7), gridspec_kw={"width_ratios": [1.8, 1]})
    colors = {"A": "#ad7e39", "B": "#087e83"}
    summaries = {row["factor"]: row for row in data["stability"]["summary"]}
    for name in ("A", "B"):
        rows = [row for row in data["stability"]["series"] if row["factor"] == name]
        summary = summaries[name]
        axes[0].plot([r["period"] for r in rows], [r["rank_ic"] for r in rows], marker="o", linewidth=2,
                     color=colors[name], label=f"{name}: mean={summary['mean_ic']:.2f}, sample SD={summary['sample_sd_ic']:.2f}")
    axes[0].axhline(.04, linestyle="--", color="#8ba4a6", linewidth=1)
    axes[0].set_xticks(range(1, 6))
    axes[0].set_xlabel("Constructed period")
    axes[0].set_ylabel("Rank IC")
    axes[0].grid(axis="y", alpha=.18)
    axes[0].legend(fontsize=8.5, loc="upper left")
    axes[1].bar(["A", "B"], [summaries[n]["icir"] for n in ("A", "B")], color=[colors[n] for n in ("A", "B")])
    for i, name in enumerate(("A", "B")):
        axes[1].text(i, summaries[name]["icir"] + .025, f"{summaries[name]['icir']:.2f}", ha="center", color=INK)
    axes[1].set_ylim(0, 1.22)
    axes[1].set_ylabel("Per-period ICIR (not annualized)")
    axes[1].grid(axis="y", alpha=.18)
    figure.suptitle("SIMULATED stability example | equal means, different variability", fontsize=14, weight="bold", color=INK)
    figure.text(.5, .015, "Two deliberately constructed five-value arrays. A higher ratio here does not establish real predictive significance.",
                ha="center", fontsize=9.5, color=MUTED)
    figure.tight_layout(rect=(0, .08, 1, .91))
    return figure


def run(input_path: Path, output: Path) -> dict:
    data = load_data(input_path)
    output = prepare_output(output)
    with plt.rc_context({"font.family": "DejaVu Sans", "svg.hashsalt": "quant-babies-lecture04",
                         "axes.spines.top": False, "axes.spines.right": False,
                         "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK}):
        files = []
        for name, function in [("factor_return_scatter", scatter_figure), ("rank_ic_series", ic_figure),
                               ("quintile_forward_returns", quintile_figure), ("factor_correlations", correlation_figure),
                               ("ic_stability", stability_figure)]:
            files.extend(save(function(data), output, name))
    return {"data_kind": data["data_kind"], "snapshot_date": data["snapshot_date"],
            "snapshot_n": data["snapshot_n"], "files": files}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="The evaluation lab's chart_data.json")
    parser.add_argument("--output", type=Path, required=True, help="A dedicated generated-figure directory")
    args = parser.parse_args()
    try:
        result = run(args.input, args.output)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Figure export failed: {exc}", file=__import__("sys").stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
