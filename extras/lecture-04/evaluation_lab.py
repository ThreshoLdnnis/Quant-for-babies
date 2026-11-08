"""Lecture 04: factor evaluation on lecture 03's unchanged SIMULATED data.

This is an offline methods exercise, not real A-share evidence or a trading backtest.
The close-to-close forward label is known only later; it is not an executable return.
Daily 20-session forward windows overlap and are not independent observations.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
from itertools import permutations
import json
import math
from pathlib import Path
import sys

import pandas as pd
import scipy
from scipy.stats import spearmanr

KEY = ["symbol", "trade_date"]
FACTORS = ["mom20", "vol20", "turn20"]
SCORES = [f"{factor}_score" for factor in FACTORS]
HORIZON = 20
MIN_N = 5
DATA_KIND = "SIMULATION_ONLY_NOT_REAL_A_SHARE_RESULTS"


def load_factor_module():
    """Use the same lecture 03 source, also supporting a downloaded sibling file."""
    folder = Path(__file__).resolve().parent
    candidates = [folder / "factor_lab.py", folder.parent / "lecture-03" / "factor_lab.py"]
    for path in candidates:
        if path.is_file():
            spec = importlib.util.spec_from_file_location("lecture03_factor_source", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module, path
    raise FileNotFoundError("Place lecture 03 factor_lab.py beside this script, or keep the repository folder structure")


def records(frame: pd.DataFrame) -> list[dict]:
    """Convert NaN to JSON null and keep a deterministic record order."""
    return json.loads(frame.to_json(orient="records", force_ascii=False, double_precision=12))


def add_future_labels(processed: pd.DataFrame, horizon: int = HORIZON) -> pd.DataFrame:
    """Add future labels after factor computation, on an already complete date grid.

    A label requires all horizon+1 prices, not only its endpoints. This is a declared
    conservative quality policy. Missing rows must be reindexed before this function.
    """
    if horizon != HORIZON:
        raise ValueError("This declared teaching label fixes horizon=20")
    frame = processed.sort_values(KEY).reset_index(drop=True).copy()
    if frame.duplicated(KEY).any() or frame[KEY].isna().any().any():
        raise ValueError("Missing or duplicate symbol/date key")
    dates_by_symbol = [tuple(group.trade_date) for _, group in frame.groupby("symbol", sort=False)]
    if not dates_by_symbol or any(dates != dates_by_symbol[0] for dates in dates_by_symbol):
        raise ValueError("Every symbol must already use the same complete ordered calendar")
    groups = frame.groupby("symbol", sort=False)
    frame["label_end_date"] = groups["trade_date"].shift(-horizon)
    frame["valid_future_prices_21"] = groups["adj_close"].transform(
        lambda s: s.iloc[::-1].rolling(horizon + 1, min_periods=1).count().iloc[::-1])
    frame["future_return_20"] = groups["adj_close"].shift(-horizon) / frame.adj_close - 1
    frame.loc[frame.valid_future_prices_21.ne(horizon + 1), "future_return_20"] = float("nan")
    usable = frame[SCORES + ["future_return_20"]].apply(
        lambda s: s.map(lambda x: pd.notna(x) and math.isfinite(x))).all(axis=1)
    frame["evaluation_common_valid"] = usable & frame["label_end_date"].notna()
    return frame


def build_labelled_panel() -> tuple[pd.DataFrame, pd.DatetimeIndex]:
    """Reuse unchanged lecture 03 inputs, factors, clipping, directions, and calendar."""
    module, _ = load_factor_module()
    raw, calendar = module.make_teaching_data()
    factors = module.compute_factors(raw, calendar, module.UNIVERSE)
    processed, _ = module.preprocess_factors(factors)
    return add_future_labels(processed), calendar


def rank_ic_one(sample: pd.DataFrame, score: str, label: str = "future_return_20",
                min_n: int = MIN_N) -> dict:
    """Spearman = Pearson of average ranks; never use the no-ties shortcut on ties."""
    pairs = sample[[score, label]].replace([float("inf"), float("-inf")], float("nan")).dropna()
    n = len(pairs)
    unique_x, unique_y = pairs[score].nunique(), pairs[label].nunique()
    result = {"n": n, "n_unique_factor": int(unique_x), "n_unique_label": int(unique_y),
              "tied_factor_rows": n - int(unique_x), "tied_label_rows": n - int(unique_y),
              "rank_ic": float("nan"), "p_value_approx": float("nan"), "status": "insufficient_n"}
    if n < min_n:
        return result
    if unique_x <= 1:
        result["status"] = "constant_factor"
        return result
    if unique_y <= 1:
        result["status"] = "constant_label"
        return result
    statistic = spearmanr(pairs[score], pairs[label])
    average_rank_corr = pairs[score].rank(method="average").corr(pairs[label].rank(method="average"))
    assert math.isclose(float(statistic.statistic), float(average_rank_corr), abs_tol=1e-12)
    result.update(rank_ic=float(statistic.statistic), p_value_approx=float(statistic.pvalue), status="ok")
    return result


def calculate_daily_ic(panel: pd.DataFrame) -> pd.DataFrame:
    """All factors use the exact same score-and-label-valid stock sample per date."""
    rows = []
    for date, daily in panel.groupby("trade_date", sort=True):
        common = daily[daily.evaluation_common_valid]
        for factor, score in zip(FACTORS, SCORES):
            rows.append({"trade_date": date, "factor": factor, **rank_ic_one(common, score)})
    return pd.DataFrame(rows)


def summarize_ic(ic: pd.DataFrame) -> pd.DataFrame:
    """Per-observation ICIR uses sample SD; no annualization or naive significance."""
    rows = []
    for factor, group in ic.groupby("factor", sort=False):
        values = group.rank_ic.dropna()
        n = len(values)
        mean = float(values.mean()) if n else float("nan")
        sd = float("nan") if n < 2 else (0.0 if values.nunique() <= 1 else float(values.std(ddof=1)))
        valid = n >= 2 and math.isfinite(sd) and sd > 0
        rows.append({"factor": factor, "n_periods": n, "mean_ic": mean, "sample_sd_ic": sd,
                     "icir": mean / sd if valid else float("nan"),
                     "positive_ic_fraction": float(values.gt(0).mean()) if n else float("nan"),
                     "status": "ok" if valid else ("insufficient_periods" if n < 2 else "zero_sd"),
                     "annualized": False, "independence_assumed": False})
    return pd.DataFrame(rows)


def quintile_analysis(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Use actual score quantiles, never split tied values by arbitrary ticker order.

    Across-date means are arithmetic averages of overlapping forward-period group
    returns, not daily portfolio returns and never input to cumprod/NAV.
    """
    assignments, returns, audits = [], [], []
    for date, daily in panel.groupby("trade_date", sort=True):
        common = daily[daily.evaluation_common_valid].copy()
        for factor, score in zip(FACTORS, SCORES):
            n, n_unique = len(common), common[score].nunique()
            audit = {"trade_date": date, "factor": factor, "n_common": n,
                     "n_unique_factor": int(n_unique), "actual_groups": 0, "status": "insufficient_n"}
            if n >= MIN_N and n_unique >= 5:
                groups = pd.qcut(common[score], 5, labels=False, duplicates="drop")
                audit["actual_groups"] = int(groups.nunique())
                if groups.nunique() == 5 and groups.notna().all():
                    assigned = common[KEY + [score, "future_return_20"]].copy()
                    assigned["factor"] = factor
                    assigned["quintile"] = groups.astype(int) + 1
                    assigned = assigned.rename(columns={score: "oriented_score"})
                    assignments.extend(records(assigned))
                    for quintile, group in assigned.groupby("quintile", sort=True):
                        returns.append({"trade_date": date, "factor": factor, "quintile": int(quintile),
                                        "n_stocks": len(group),
                                        "mean_forward_return_20": float(group.future_return_20.mean())})
                    audit["status"] = "ok"
                else:
                    audit["status"] = "fewer_than_five_quantile_bins"
            elif n >= MIN_N:
                audit["status"] = "insufficient_unique_values"
            audits.append(audit)
    columns = ["trade_date", "factor", "quintile", "n_stocks", "mean_forward_return_20"]
    periodic = pd.DataFrame(returns, columns=columns)
    if periodic.empty:
        mean = pd.DataFrame(columns=["factor", "quintile", "mean_forward_return_20", "mean_n_stocks", "n_periods"])
    else:
        mean = periodic.groupby(["factor", "quintile"], sort=True).agg(
            mean_forward_return_20=("mean_forward_return_20", "mean"),
            mean_n_stocks=("n_stocks", "mean"), n_periods=("trade_date", "count")).reset_index()
    return pd.DataFrame(assignments), periodic, mean, pd.DataFrame(audits)


def split_audit(panel: pd.DataFrame, calendar: pd.DatetimeIndex) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fixed [0,40), [40,60), [60,80) split; purge labels ending outside their split.

    Past feature history may precede the split. The deliberately short dataset leaves
    no usable fully matured factor-label pairs in these three formal split segments.
    """
    rows, summaries = [], []
    for name, start, stop in [("development", 0, 40), ("validation", 40, 60), ("test", 60, 80)]:
        first, last = str(calendar[start].date()), str(calendar[stop - 1].date())
        subset = panel[panel.trade_date.between(first, last)].copy()
        mature = subset.label_end_date.notna() & subset.label_end_date.le(last)
        feature_valid = subset[SCORES].notna().all(axis=1)
        eligible = subset.evaluation_common_valid & mature
        subset["split"] = name
        subset["split_end_date"] = last
        subset["label_mature_within_split"] = mature & subset.future_return_20.notna()
        subset["usable_for_split"] = eligible
        subset["split_label_status"] = "unavailable_label"
        subset.loc[subset.label_end_date.isna(), "split_label_status"] = "no_future_endpoint"
        subset.loc[subset.label_end_date.notna() & subset.label_end_date.gt(last), "split_label_status"] = "crosses_split_end"
        subset.loc[mature & subset.future_return_20.notna(), "split_label_status"] = "mature_within_split"
        rows.extend(records(subset[KEY + ["split", "label_end_date", "split_end_date", "split_label_status",
                                           "label_mature_within_split", "usable_for_split"]]))
        daily_counts = subset.loc[eligible].groupby("trade_date").size()
        summaries.append({"split": name, "start_index": start, "stop_index_exclusive": stop,
                          "start_date": first, "end_date": last, "n_dates": stop - start,
                          "n_rows": len(subset), "feature_ready_rows": int(feature_valid.sum()),
                          "mature_label_rows": int(subset.label_mature_within_split.sum()),
                          "usable_factor_label_rows": int(eligible.sum()),
                          "dates_with_at_least_five_pairs": int(daily_counts.ge(MIN_N).sum()),
                          "status": "insufficient_matured_pairs" if not daily_counts.ge(MIN_N).any() else "available"})
    return pd.DataFrame(rows), pd.DataFrame(summaries)


def common_quintile_summary(periodic: pd.DataFrame, audit: pd.DataFrame
                            ) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    """Intersect valid grouping calendars by a predeclared rule, not by returns."""
    eligible = [set(audit.loc[audit.factor.eq(factor) & audit.status.eq("ok"), "trade_date"])
                for factor in FACTORS]
    dates = sorted(set.intersection(*eligible))
    common = periodic[periodic.trade_date.isin(dates)].copy()
    mean = common.groupby(["factor", "quintile"], sort=True).agg(
        mean_forward_return_20=("mean_forward_return_20", "mean"),
        mean_n_stocks=("n_stocks", "mean"), n_periods=("trade_date", "count")).reset_index()
    return common, mean, dates


def manual_rank_example() -> tuple[pd.DataFrame, dict]:
    """The user's five-stock example plus an exhaustive classroom permutation test."""
    frame = pd.DataFrame({"symbol": list("ABCDE"), "factor": [.12, .04, -.03, .08, .01],
                          "future_return": [.05, -.01, -.04, .07, .02]})
    frame["factor_rank"] = frame.factor.rank(method="average")
    frame["return_rank"] = frame.future_return.rank(method="average")
    frame["rank_difference"] = frame.factor_rank - frame.return_rank
    frame["difference_squared"] = frame.rank_difference ** 2
    statistic = spearmanr(frame.factor, frame.future_return)
    observed = float(statistic.statistic)
    null = [float(spearmanr(frame.factor, values).statistic) for values in permutations(frame.future_return)]
    extreme = sum(abs(value) >= abs(observed) - 1e-12 for value in null)
    return frame, {"n": 5, "sum_d_squared": float(frame.difference_squared.sum()), "rank_ic": observed,
                   "scipy_p_value_approx": float(statistic.pvalue), "permutations": len(null),
                   "extreme_permutations_two_sided": extreme, "exact_permutation_p_two_sided": extreme / len(null),
                   "permutation_assumption": "Classroom null: return labels are exchangeable across these five stocks; not a real-market independence claim",
                   "plus_one_correction": False, "p_value_note": "Exhaustive 120 permutations; SciPy default is approximate for this small sample"}


def stability_example() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Construct equal means, then calculate actual sample SD and ICIR from arrays."""
    rows = []
    a_values = [-.10, .02, .04, .06, .18]
    for name, values in [("A", a_values), ("B", [.04 + .4 * (value - .04) for value in a_values])]:
        rows.extend({"factor": name, "period": i + 1, "rank_ic": value} for i, value in enumerate(values))
    series = pd.DataFrame(rows)
    return series, summarize_ic(series)


def validate_definitions(panel: pd.DataFrame, calendar: pd.DatetimeIndex, ic: pd.DataFrame,
                         group_returns: pd.DataFrame, group_audit: pd.DataFrame,
                         split_rows: pd.DataFrame, split_summary: pd.DataFrame) -> dict:
    """Independent hand calculations and edge cases; no performance-based tuning."""
    manual, stats = manual_rank_example()
    assert stats["sum_d_squared"] == 4 and math.isclose(stats["rank_ic"], .8, abs_tol=1e-12)
    assert stats["permutations"] == 120 and stats["extreme_permutations_two_sided"] == 16
    assert math.isclose(stats["exact_permutation_p_two_sided"], 2 / 15, abs_tol=1e-12)
    ties = pd.DataFrame({"x": [1., 1., 2., 3., 4.], "y": [4., 3., 2., 1., 0.]})
    tie_result = rank_ic_one(ties, "x", "y")
    assert tie_result["status"] == "ok" and tie_result["tied_factor_rows"] == 1
    assert math.isclose(tie_result["rank_ic"], ties.x.rank().corr(ties.y.rank()), abs_tol=1e-12)
    constant = pd.DataFrame({"x": [.1] * 6, "y": range(6)})
    assert rank_ic_one(constant, "x", "y")["status"] == "constant_factor"
    assert rank_ic_one(constant.rename(columns={"x": "y", "y": "x"}), "x", "y")["status"] == "constant_label"
    missing = pd.DataFrame({"x": [1., 2., 3., 4., float("nan")], "y": [5., 4., 3., 2., 1.]})
    assert rank_ic_one(missing, "x", "y")["status"] == "insufficient_n"
    zero = summarize_ic(pd.DataFrame({"factor": "X", "rank_ic": [.1] * 6})).iloc[0]
    assert zero["status"] == "zero_sd" and pd.isna(zero.icir)
    for _, stock in panel.groupby("symbol"):
        assert stock.future_return_20.iloc[-HORIZON:].isna().all()
    dates = pd.bdate_range("2024-01-02", periods=45)
    toy = pd.DataFrame([{"symbol": symbol, "trade_date": str(d.date()), "adj_close": base + i * step,
                         **{score: float(i) for score in SCORES}}
                        for symbol, base, step in [("A", 10., .1), ("B", 100., 0.)]
                        for i, d in enumerate(dates)])
    labelled = add_future_labels(toy)
    a = labelled[labelled.symbol.eq("A")].reset_index(drop=True)
    b = labelled[labelled.symbol.eq("B")].reset_index(drop=True)
    assert math.isclose(a.loc[0, "future_return_20"], .2, abs_tol=1e-12)
    assert b.future_return_20.iloc[:25].eq(0).all()
    toy.loc[toy.symbol.eq("A") & toy.trade_date.eq(str(dates[10].date())), "adj_close"] = float("nan")
    gap = add_future_labels(toy)
    ga = gap[gap.symbol.eq("A")].reset_index(drop=True)
    assert ga.future_return_20.iloc[:11].isna().all() and ga.future_return_20.iloc[11:25].notna().all()
    assert ic.groupby("trade_date").n.nunique().eq(1).all()
    counts = group_returns.groupby(["trade_date", "factor"]).n_stocks.sum()
    valid_audit = group_audit[group_audit.status.eq("ok")].set_index(["trade_date", "factor"])
    assert counts.sort_index().equals(valid_audit.n_common.rename("n_stocks").sort_index())
    tied_panel = panel[panel.trade_date.eq(str(calendar[20].date()))].copy()
    tied_panel.loc[:, SCORES] = 1.
    _, tied_returns, _, tied_audit = quintile_analysis(tied_panel)
    assert tied_returns.empty and tied_audit.status.eq("insufficient_unique_values").all()
    assert split_summary.usable_factor_label_rows.eq(0).all()
    usable = split_rows[split_rows.usable_for_split]
    assert usable.empty or usable.label_end_date.le(usable.split_end_date).all()
    _, stability = stability_example()
    assert all(math.isclose(x, y, abs_tol=1e-12) for x, y in zip(stability.mean_ic, [.04, .04]))
    assert all(math.isclose(x, y, abs_tol=1e-12) for x, y in zip(stability.sample_sd_ic, [.10, .04]))
    assert all(math.isclose(x, y, abs_tol=1e-12) for x, y in zip(stability.icir, [.4, 1.]))
    module, _ = load_factor_module()
    raw, _ = module.make_teaching_data()
    cutoff = str(calendar[-5].date())
    future = raw.copy()
    future.loc[future.trade_date.ge(cutoff), "adj_close"] *= 1.2
    future.loc[future.trade_date.ge(cutoff), "turnover_rate"] *= 1.6
    recomputed, _ = module.preprocess_factors(module.compute_factors(future, calendar, module.UNIVERSE))
    columns = KEY + FACTORS + SCORES
    pd.testing.assert_frame_equal(panel.loc[panel.trade_date.lt(cutoff), columns].reset_index(drop=True),
                                  recomputed.loc[recomputed.trade_date.lt(cutoff), columns].reset_index(drop=True))
    nonoverlap = calendar[20:len(calendar) - HORIZON:HORIZON]
    assert len(nonoverlap) == 2
    assert len(panel) == 640 and not panel.duplicated(KEY).any()
    return {"manual_rank_ic_0_8": True, "exhaustive_permutation_16_of_120": True,
            "ties_use_average_ranks": True, "constant_factor_and_label_undefined": True,
            "missing_pairs_and_min_n": True, "zero_sd_icir_is_missing": True,
            "last_twenty_labels_missing": True, "future_gap_propagates_without_fill": True,
            "future_shift_stays_within_stock": True, "same_pair_sample_for_all_factors": True,
            "quintile_counts_match_common_sample": True, "tied_values_not_split_arbitrarily": True,
            "fixed_splits_purge_cross_boundary_labels": True, "insufficient_formal_splits_reported": True,
            "icir_stability_arrays_match_statistics": True, "future_changes_preserve_past_factors": True,
            "nonoverlap_grid_predeclared": True, "complete_unique_640_row_grid": True}


def run(output: Path) -> dict:
    output = output.resolve()
    marker = output / ".quant_babies_lecture04_evaluation"
    if output.exists() and not output.is_dir():
        raise FileExistsError(f"Not a directory: {output}")
    if output.exists() and any(output.iterdir()) and not marker.exists():
        raise FileExistsError(f"Refusing to overwrite a non-lab directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    marker.write_text("SIMULATED factor evaluation only; no trading backtest.\n", encoding="utf-8")
    module, module_path = load_factor_module()
    raw, calendar = module.make_teaching_data()
    factors = module.compute_factors(raw, calendar, module.UNIVERSE)
    processed, pre_audit = module.preprocess_factors(factors)
    panel = add_future_labels(processed)
    raw.to_csv(output / "raw_simulated.csv", index=False)
    pd.DataFrame({"trade_date": calendar.strftime("%Y-%m-%d")}).to_csv(output / "calendar_simulated.csv", index=False)
    processed.to_csv(output / "factors_before_labels.csv", index=False)
    panel.to_csv(output / "labelled_panel.csv", index=False)
    pre_audit.to_csv(output / "preprocessing_audit.csv", index=False)
    module.factor_definitions().to_csv(output / "factor_definitions.csv", index=False)
    ic = calculate_daily_ic(panel)
    summary = summarize_ic(ic)
    nonoverlap_dates = set(calendar[20:len(calendar) - HORIZON:HORIZON].strftime("%Y-%m-%d"))
    nonoverlap_ic = ic[ic.trade_date.isin(nonoverlap_dates)].copy()
    nonoverlap_summary = summarize_ic(nonoverlap_ic)
    assignments, periodic, quintile_mean, quintile_audit = quintile_analysis(panel)
    periodic_common, quintile_mean_common, common_quintile_dates = common_quintile_summary(periodic, quintile_audit)
    split_rows, splits = split_audit(panel, calendar)
    manual, manual_stats = manual_rank_example()
    stability_series, stability_summary = stability_example()
    snapshot_date = str(calendar[-HORIZON - 1].date())
    snapshot = panel[panel.trade_date.eq(snapshot_date) & panel.evaluation_common_valid].sort_values("symbol")
    # Redundancy is contemporaneous: never require a future label to screen this sample.
    factor_snapshot = panel[panel.trade_date.eq(snapshot_date) & panel[SCORES].notna().all(axis=1)].sort_values("symbol")
    correlation = factor_snapshot[SCORES].corr(method="pearson", min_periods=MIN_N)
    correlation.index = FACTORS
    correlation.columns = FACTORS
    frames = {"daily_ic": ic, "ic_summary": summary, "nonoverlap_ic": nonoverlap_ic,
              "nonoverlap_ic_summary": nonoverlap_summary, "quintile_assignments": assignments,
              "quintile_returns": periodic, "quintile_mean": quintile_mean, "quintile_audit": quintile_audit,
              "quintile_returns_common": periodic_common, "quintile_mean_common": quintile_mean_common,
              "split_rows": split_rows, "split_summary": splits, "manual_ranks": manual,
              "stability_series": stability_series, "stability_summary": stability_summary}
    for name, frame in frames.items():
        frame.to_csv(output / f"{name}.csv", index=False)
    correlation.to_csv(output / "correlation_scores.csv", index_label="factor")
    checks = validate_definitions(panel, calendar, ic, periodic, quintile_audit, split_rows, splits)
    expected_common = set.intersection(*[set(quintile_audit.loc[
        quintile_audit.factor.eq(factor) & quintile_audit.status.eq("ok"), "trade_date"]) for factor in FACTORS])
    assert set(common_quintile_dates) == expected_common
    assert quintile_mean_common.n_periods.eq(len(common_quintile_dates)).all()
    checks["common_quintile_calendar_is_rule_intersection"] = True
    assert all(checks.values())
    inference_note = "Daily 20-session labels overlap; no naive t-test or independent-date confidence interval. Two predeclared nonoverlapping observations are too few for inference."
    charts = {"data_kind": DATA_KIND, "factor_names": FACTORS, "score_columns": SCORES,
              "horizon": HORIZON, "label": "future_return_20", "label_unit": "decimal price return",
              "label_note": "t close to t+20 close; evaluation label, not executable strategy return",
              "calendar_note": "80 pandas business dates, not an A-share exchange calendar",
              "snapshot_date": snapshot_date, "snapshot_n": len(snapshot),
              "manual": {**manual_stats, "ranks": records(manual)},
              "snapshot": records(snapshot[KEY + SCORES + ["future_return_20"]]),
              "ic_series": records(ic), "ic_summary": records(summary),
              "nonoverlap_ic_summary": records(nonoverlap_summary),
              "quintile_mean": records(quintile_mean), "quintile_returns": records(periodic),
              "quintile_mean_common": records(quintile_mean_common),
              "common_quintile_dates": common_quintile_dates,
              "common_quintile_n_dates": len(common_quintile_dates),
              "correlation": {"n_common": len(factor_snapshot), "labels": FACTORS, "stage": "fixed oriented Z-scores",
                              "sample_note": "Current factor-valid stocks only; no future-label screening",
                              "symbols": factor_snapshot.symbol.tolist(),
                              "score_values": factor_snapshot[SCORES].T.values.tolist(),
                              "matrix": json.loads(correlation.to_json(orient="values", double_precision=12))},
              "stability": {"series": records(stability_series), "summary": records(stability_summary)},
              "splits": records(splits), "inference_note": inference_note}
    (output / "chart_data.json").write_text(json.dumps(charts, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    report = {"data_kind": DATA_KIND, "input_rows": len(raw), "grid_rows": len(panel),
              "calendar_dates": len(calendar), "symbols": len(module.UNIVERSE),
              "factor_source_sha256": hashlib.sha256(module_path.read_bytes()).hexdigest(),
              "input_sha256": hashlib.sha256((output / "raw_simulated.csv").read_bytes()).hexdigest(),
              "horizon": HORIZON, "min_n": MIN_N, "sample_policy": "same date, all three fixed scores and future label jointly finite",
              "future_label_nonmissing_rows": int(panel.future_return_20.notna().sum()),
              "evaluation_common_rows": int(panel.evaluation_common_valid.sum()),
              "ic_rows": len(ic), "valid_ic_rows": int(ic.status.eq("ok").sum()),
              "valid_ic_dates": int(ic.loc[ic.status.eq("ok"), "trade_date"].nunique()),
              "nonoverlap_dates": sorted(nonoverlap_dates), "snapshot_date": snapshot_date,
              "snapshot_common_n": len(snapshot), "quintile_status_counts": quintile_audit.status.value_counts().to_dict(),
              "quintile_available_dates_by_factor": {factor: int(quintile_audit.loc[
                  quintile_audit.factor.eq(factor) & quintile_audit.status.eq("ok")].shape[0]) for factor in FACTORS},
              "common_quintile_n_dates": len(common_quintile_dates),
              "common_quintile_sample_note": "Intersection of dates where every factor forms five actual quantile bins; not selected by return performance",
              "formal_split_usable_pairs": {row["split"]: row["usable_factor_label_rows"] for row in records(splits)},
              "icir_ddof": 1, "icir_annualized": False, "p_values": manual_stats,
              "inference_note": inference_note, "checks": checks,
              "pandas_version": pd.__version__, "scipy_version": scipy.__version__}
    (output / "quality_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/processed/lecture04-simulation"))
    args = parser.parse_args()
    try:
        report = run(args.output)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Evaluation lab failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({key: report[key] for key in ["data_kind", "grid_rows", "valid_ic_dates", "snapshot_date",
                                                "snapshot_common_n", "formal_split_usable_pairs", "checks"]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
