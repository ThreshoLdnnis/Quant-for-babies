"""Export lecture 03's SIMULATED factor figures using matplotlib, without network access.

First run factor_lab.py. Then pass its chart_data.json through --input.
PNG and SVG are saved to a dedicated directory; unrelated contents are protected.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np


FACTORS = ["mom20", "vol20", "turn20"]
LABELS = {
    "mom20": "MOM20: price return (%)",
    "vol20": "VOL20: daily sample standard deviation (%)",
    "turn20": "TURN20: average turnover (%)",
}


def load_data(path: Path) -> dict:
    """Accept only the explicit simulation export produced by this course."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("data_kind") != "SIMULATION_ONLY_NOT_REAL_A_SHARE_RESULTS":
        raise ValueError("Expected explicitly SIMULATED lecture 03 chart data")
    if data.get("factor_names") != FACTORS or data["correlation"]["labels"] != FACTORS:
        raise ValueError("Unexpected factor order")
    n = data["correlation"]["n_common"]
    if n < 2 or n != len(data["symbols"]):
        raise ValueError("Expected at least two common stocks and matching labels")
    for factor in FACTORS:
        entry = data["distributions"][factor]
        if entry["symbols"] != data["symbols"]:
            raise ValueError("Factor samples are not aligned")
        for kind in ("raw", "clipped", "z"):
            values = np.asarray(entry[kind], dtype=float)
            if len(values) != n or not np.isfinite(values).all():
                raise ValueError(f"Nonfinite or inconsistent {factor}/{kind}")
    for kind in ("raw", "z"):
        matrix = np.asarray(data["correlation"][kind], dtype=float)
        if matrix.shape != (3, 3) or not np.isfinite(matrix).all():
            raise ValueError("Expected a finite 3 by 3 correlation matrix")
        values = np.asarray([data["distributions"][factor][kind] for factor in FACTORS])
        if not np.allclose(matrix, np.corrcoef(values), atol=1e-9, rtol=1e-9):
            raise ValueError("Exported matrix does not match the common factor sample")
    return data


def prepare_output(output: Path) -> Path:
    """Only overwrite figures in a directory marked as this plotting experiment."""
    output = output.resolve()
    marker = output / ".quant_babies_lecture03_plots"
    if output.exists() and not output.is_dir():
        raise FileExistsError(f"Not a directory: {output}")
    if output.exists() and any(output.iterdir()) and not marker.exists():
        raise FileExistsError(f"Refusing to overwrite a non-plot directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    marker.write_text("SIMULATED lecture 03 figures only.\n", encoding="utf-8")
    return output


def save_figure(figure, output: Path, name: str) -> list[Path]:
    files = []
    for extension in ("png", "svg"):
        path = output / f"{name}.{extension}"
        metadata = {"Date": None} if extension == "svg" else {"Software": "Quant for Babies / matplotlib"}
        figure.savefig(path, dpi=180, bbox_inches="tight", facecolor="white", metadata=metadata)
        files.append(path)
    plt.close(figure)
    return files


def distribution_figure(data: dict):
    """Raw/clipped panels share bins and axis ranges within each factor row."""
    n = data["correlation"]["n_common"]
    figure, axes = plt.subplots(3, 2, figsize=(12.2, 10.4), sharey="row")
    for row, factor in enumerate(FACTORS):
        raw = 100 * np.asarray(data["distributions"][factor]["raw"], dtype=float)
        clipped = 100 * np.asarray(data["distributions"][factor]["clipped"], dtype=float)
        combined = np.concatenate([raw, clipped])
        low, high = combined.min(), combined.max()
        padding = (high - low) * 0.05 if high > low else max(abs(low) * 0.05, 0.1)
        bins = np.linspace(low - padding, high + padding, 7)
        counts = [np.histogram(values, bins=bins)[0] for values in (raw, clipped)]
        ymax = max(int(c.max()) for c in counts) + 1
        for column, (values, title, color) in enumerate([
            (raw, "Raw values", "#087e83"), (clipped, "After median +/- 3 raw MAD", "#b17f3a")
        ]):
            axis = axes[row, column]
            axis.hist(values, bins=bins, color=color, edgecolor="white", linewidth=1)
            axis.axvline(float(np.median(values)), color="#193346", linestyle="--", linewidth=1,
                         label="Median")
            axis.set_title(title, fontsize=11)
            axis.set_xlabel(LABELS[factor], fontsize=10)
            axis.set_xlim(bins[0], bins[-1])
            axis.set_ylim(0, ymax)
            axis.yaxis.set_major_locator(MaxNLocator(integer=True))
            axis.grid(axis="y", color="#dfe6e3", linewidth=0.6)
            axis.set_axisbelow(True)
            if column == 0:
                axis.set_ylabel("Stock count")
            axis.legend(fontsize=8, frameon=False)
    figure.suptitle(f"SIMULATED factor distributions | {data['snapshot_date']} | common n={n}",
                   fontsize=15, fontweight="bold", color="#193346")
    figure.text(0.5, 0.015,
        f"Small teaching sample (n={n}): bars describe this cross-section, not a population distribution.\n"
        "Bins and axes match within each row. Raw MAD is unscaled; no 1.4826 multiplier. No annualization.",
        ha="center", va="bottom", fontsize=9, color="#526a79")
    figure.tight_layout(rect=(0, 0.07, 1, 0.95), h_pad=2.2)
    return figure


def correlation_figure(data: dict):
    """Use identical Pearson color scales, dates, factor order and common samples."""
    n = data["correlation"]["n_common"]
    figure, axes = plt.subplots(1, 2, figsize=(11.5, 5.8))
    for axis, kind, title in zip(axes, ("raw", "z"), ("Raw factors", "MAD-clipped, Z-score factors")):
        matrix = np.asarray(data["correlation"][kind], dtype=float)
        image = axis.imshow(matrix, cmap="coolwarm", vmin=-1, vmax=1, interpolation="nearest")
        axis.set_xticks(range(3), [f.upper() for f in FACTORS])
        axis.set_yticks(range(3), [f.upper() for f in FACTORS])
        axis.set_title(title, fontsize=12, pad=13)
        for i in range(3):
            for j in range(3):
                value = matrix[i, j]
                axis.text(j, i, f"{value:+.2f}", ha="center", va="center", fontsize=13,
                          color="white" if abs(value) >= 0.7 else "#193346")
    figure.suptitle(f"SIMULATED cross-sectional Pearson correlation | {data['snapshot_date']} | n={n}",
                   fontsize=14, fontweight="bold", color="#193346")
    figure.subplots_adjust(left=0.07, right=0.87, bottom=0.20, top=0.82, wspace=0.35)
    color_axis = figure.add_axes((0.90, 0.24, 0.022, 0.53))
    figure.colorbar(image, cax=color_axis, ticks=[-1, -0.5, 0, 0.5, 1], label="Pearson r")
    figure.text(0.5, 0.05,
        "Same common stocks in both panels. Z-score alone does not change Pearson correlation; clipping can.\n"
        "One small fictional cross-section is not evidence of predictive ability. No real A-share results.",
        ha="center", va="bottom", fontsize=9, color="#526a79")
    return figure


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="chart_data.json from factor_lab.py")
    parser.add_argument("--output", type=Path, default=Path("data/processed/lecture-03-plots"),
                        help="Dedicated figure output directory; unrelated nonempty directories are refused")
    args = parser.parse_args()
    data = load_data(args.input)
    output = prepare_output(args.output)
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 10, "svg.fonttype": "none",
                         "svg.hashsalt": "quant-babies-lecture03"}):
        files = save_figure(distribution_figure(data), output, "factor_distributions")
        files += save_figure(correlation_figure(data), output, "factor_correlations")
    print(json.dumps({"data_kind": data["data_kind"], "files": [str(p) for p in files]}, indent=2))


if __name__ == "__main__":
    main()
