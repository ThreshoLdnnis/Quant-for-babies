"""第三讲：离线量价因子构建与逐日横截面预处理。

全部数值属于确定性模拟，不是真实 A 股结果。80 个 pandas 工作日不是
交易所日历；SIM001/SIM002 的基础价格和量沿用第二讲生成公式后扩展。
模拟没有公司行为，adj_close 等于原始报价，不冒充真实复权快照。
本程序只演示因子工程，不计算 IC、策略持仓、回测或机器学习结果。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import pandas as pd


KEY = ["symbol", "trade_date"]
FACTORS = ["mom20", "vol20", "turn20"]
DIRECTIONS = {"mom20": 1, "vol20": -1, "turn20": -1}
MIN_N = 5
MAD_K = 3.0
UNIVERSE = [f"SIM{i:03d}" for i in range(1, 9)]
DATA_KIND = "SIMULATION_ONLY_NOT_REAL_A_SHARE_RESULTS"


def make_teaching_data() -> tuple[pd.DataFrame, pd.DatetimeIndex]:
    """八只虚构证券、80 个模拟工作日；刻意保留少量未知值与缺行。

    SIM001/SIM002 沿用第二讲的底层 price/volume 公式，不沿用第二讲用于
    数据清洗演示的全部脏记录。本讲缺失由 status 明确说明。其余六只为
    横截面统计补充有差异的模拟路径，SIM008 刻意具有较极端的数值。
    """
    dates = pd.bdate_range("2024-01-02", periods=80)
    records = []
    for stock_no, symbol in enumerate(UNIVERSE):
        for i, date in enumerate(dates):
            if stock_no < 2:
                price = round(10 + stock_no * 10 + i * 0.06 + (i % 5 - 2) * 0.03, 2)
                volume = 10000 + stock_no * 2000 + i * 100
            else:
                base = 12 + stock_no * 4.5
                drift = (stock_no - 3.8) * 0.00055
                amplitude = 0.018 + stock_no * 0.003
                if symbol == "SIM008":
                    amplitude = 0.085
                price = round(base * math.exp(drift * i + amplitude * math.sin(i * (0.31 + stock_no * 0.02))), 4)
                if symbol == "SIM008" and i >= 60:
                    price = round(price * (1 + 0.028 * (i - 59)), 4)
                volume = int((12000 + stock_no * 1800 + 45 * i) * (1 + 0.23 * math.sin(i * 0.27 + stock_no)))
            free_float_shares = 700000 + stock_no * 130000
            turnover = volume / free_float_shares
            if symbol == "SIM008" and i >= 60:
                volume = int(free_float_shares * (0.16 + 0.015 * math.sin(i)))
                turnover = volume / free_float_shares
            records.append({
                "symbol": symbol, "trade_date": date.strftime("%Y-%m-%d"),
                "close_raw": price, "adj_close": price,
                "volume": volume, "free_float_shares": free_float_shares,
                "turnover_rate": turnover, "status": "observed_simulation",
                "in_universe": True, "is_simulated": True,
            })
    raw = pd.DataFrame.from_records(records)
    # 停牌状态是本实验预先设定的事实，不能从普通缺行自动推断。
    suspended = raw.symbol.eq("SIM002") & raw.trade_date.eq(str(dates[10].date()))
    raw.loc[suspended, ["close_raw", "adj_close"]] = float("nan")
    raw.loc[suspended, ["volume", "turnover_rate"]] = 0
    raw.loc[suspended, "status"] = "known_simulated_suspension"
    price_gap = raw.symbol.eq("SIM001") & raw.trade_date.eq(str(dates[30].date()))
    raw.loc[price_gap, ["close_raw", "adj_close"]] = float("nan")
    raw.loc[price_gap, "status"] = "unresolved_missing_price"
    turnover_gap = raw.symbol.eq("SIM003") & raw.trade_date.eq(str(dates[35].date()))
    raw.loc[turnover_gap, "turnover_rate"] = float("nan")
    raw.loc[turnover_gap, "status"] = "unknown_turnover"
    missing_bar = raw.symbol.eq("SIM004") & raw.trade_date.eq(str(dates[45].date()))
    raw = raw.loc[~missing_bar].sample(frac=1, random_state=3).reset_index(drop=True)
    return raw, dates


def compute_factors(input_frame: pd.DataFrame, calendar: pd.DatetimeIndex,
                    universe: list[str]) -> pd.DataFrame:
    """在明确日历网格中计算严格的 20 期指标，缺失价格不做任何填补。

    实际项目应传入经过核对的交易所日历、历史股票池、复权口径与状态表。
    本课 CLI 仅生成模拟数据，避免把 pandas 工作日当作真实 A 股日历。
    MOM20 另要求 21 个连续有效价格，VOL20 要求 20 个有效日收益，
    TURN20 要求 20 个有效换手率。三个指标的满窗口条件不同。
    """
    required = set(KEY + ["adj_close", "turnover_rate"])
    if not required.issubset(input_frame.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(input_frame.columns))}")
    calendar = pd.DatetimeIndex(pd.to_datetime(calendar)).normalize()
    if len(calendar) == 0 or calendar.has_duplicates or not calendar.is_monotonic_increasing:
        raise ValueError("calendar must be nonempty, unique, and increasing")
    if len(universe) != len(set(universe)) or not universe:
        raise ValueError("universe must contain distinct symbols")
    work = input_frame.copy()
    work["symbol"] = work.symbol.astype("string")
    work["trade_date"] = pd.to_datetime(work.trade_date, errors="raise")
    if work[KEY].isna().any().any() or work.duplicated(KEY).any():
        raise ValueError("Missing or duplicate symbol/date key")
    if not work.symbol.isin(universe).all() or not work.trade_date.isin(calendar).all():
        raise ValueError("Input contains symbols/dates outside the declared grid")
    for column in ("adj_close", "turnover_rate"):
        work[column] = pd.to_numeric(work[column], errors="raise")
        values = work[column].dropna()
        if not values.map(math.isfinite).all():
            raise ValueError(f"Nonfinite {column}")
    if (work.adj_close.dropna() <= 0).any() or (work.turnover_rate.dropna() < 0).any():
        raise ValueError("This positive-price simulation expects price > 0 and turnover >= 0")
    grid = pd.MultiIndex.from_product([universe, calendar], names=KEY)
    result = work.set_index(KEY).reindex(grid).reset_index()
    result["status"] = result.get("status", pd.Series(index=result.index, dtype="object")).fillna("missing_record")
    # 本模拟所有证券在整个日期网格均属于预先声明的研究池。
    if "in_universe" not in result:
        result["in_universe"] = True
    else:
        result["in_universe"] = result["in_universe"].fillna(True).astype(bool)
    groups = result.groupby("symbol", sort=False)
    result["ret_1d"] = groups["adj_close"].pct_change(fill_method=None)
    result["valid_prices_21"] = groups["adj_close"].transform(
        lambda s: s.rolling(21, min_periods=1).count())
    result["valid_returns_20"] = result.groupby("symbol")["ret_1d"].transform(
        lambda s: s.rolling(20, min_periods=1).count())
    result["valid_turnover_20"] = groups["turnover_rate"].transform(
        lambda s: s.rolling(20, min_periods=1).count())
    result["mom20"] = result.adj_close / groups["adj_close"].shift(20) - 1
    result.loc[result.valid_prices_21 < 21, "mom20"] = float("nan")
    result["vol20"] = result.groupby("symbol")["ret_1d"].transform(
        lambda s: s.rolling(20, min_periods=20).std(ddof=1))
    result["turn20"] = groups["turnover_rate"].transform(
        lambda s: s.rolling(20, min_periods=20).mean())
    result["trade_date"] = result.trade_date.dt.strftime("%Y-%m-%d")
    return result


def preprocess_factors(factors: pd.DataFrame, min_n: int = MIN_N,
                       mad_k: float = MAD_K, directions: dict | None = None
                       ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """逐日、共同有效股票样本上做 raw MAD 裁剪、总体标准差 Z-score 与方向。

    MAD = median(abs(x - median(x)))，不乘 1.4826。MAD 为零时保留原值并
    在 audit 标记。Z-score 使用 ddof=0；n<min_n 或标准差为零则得分缺失。
    方向为教学研究假设，不使用未来标签选择。非共同样本不参与任一因子处理。
    """
    directions = DIRECTIONS.copy() if directions is None else dict(directions)
    if min_n < 2 or not math.isfinite(mad_k) or mad_k <= 0:
        raise ValueError("min_n >= 2 and finite mad_k > 0 are required")
    if set(directions) != set(FACTORS) or any(x not in (-1, 1) for x in directions.values()):
        raise ValueError("directions must give +1/-1 for every factor")
    output = factors.copy()
    if output.duplicated(KEY).any():
        raise ValueError("Duplicate factor keys")
    finite = output[FACTORS].apply(lambda s: s.map(lambda x: pd.notna(x) and math.isfinite(x))).all(axis=1)
    membership = output["in_universe"] if "in_universe" in output else pd.Series(True, index=output.index)
    domain_valid = output["vol20"].ge(0) & output["turn20"].ge(0)
    output["common_valid"] = finite & domain_valid & membership.fillna(False).astype(bool)
    output["cross_section_n"] = output.groupby("trade_date")["common_valid"].transform("sum")
    for factor in FACTORS:
        for suffix in ("clip", "z", "score"):
            output[f"{factor}_{suffix}"] = float("nan")
    audit = []
    for date, indexes in output.groupby("trade_date", sort=True).groups.items():
        valid_indexes = output.index[output.index.isin(indexes) & output.common_valid]
        n = len(valid_indexes)
        for factor in FACTORS:
            raw = output.loc[valid_indexes, factor].astype(float)
            median = raw.median() if n else float("nan")
            mad = (raw - median).abs().median() if n else float("nan")
            row = {"trade_date": date, "factor": factor, "n": n,
                   "median": median, "mad": mad,
                   "lower": median - mad_k * mad, "upper": median + mad_k * mad,
                   "mad_zero": bool(n and mad == 0), "clip_count": 0,
                   "mean_clip": float("nan"), "std_clip": float("nan"),
                   "z_status": "insufficient_n", "direction": directions[factor]}
            if n >= min_n:
                clipped = raw.copy() if mad == 0 else raw.clip(row["lower"], row["upper"])
                mean = clipped.mean()
                # Identical floating values are constant even when summation rounds the mean.
                sd = 0.0 if clipped.nunique() <= 1 else clipped.std(ddof=0)
                output.loc[valid_indexes, f"{factor}_clip"] = clipped
                row.update(clip_count=int(clipped.ne(raw).sum()), mean_clip=mean, std_clip=sd)
                if sd == 0 or not math.isfinite(sd):
                    row["z_status"] = "zero_std"
                else:
                    z = (clipped - mean) / sd
                    output.loc[valid_indexes, f"{factor}_z"] = z
                    output.loc[valid_indexes, f"{factor}_score"] = directions[factor] * z
                    row["z_status"] = "ok"
            audit.append(row)
    return output, pd.DataFrame.from_records(audit)


def factor_definitions() -> pd.DataFrame:
    """可交付的因子数据字典，明确单位、窗口、时点和模拟边界。"""
    return pd.DataFrame([
        {"factor": "mom20", "formula": "P[t]/P[t-20]-1", "unit": "decimal return",
         "history": "21 consecutive valid prices", "statistic_ddof": "not applicable", "annualized": False,
         "direction": 1, "available_at": "after t close", "meaning": "20-period price momentum"},
        {"factor": "vol20", "formula": "sample_std(r[t-19:t])", "unit": "decimal return",
         "history": "20 consecutive valid one-period returns (21 prices)", "statistic_ddof": "1", "annualized": False,
         "direction": -1, "available_at": "after t close", "meaning": "historical daily return dispersion"},
        {"factor": "turn20", "formula": "mean(turnover[t-19:t])", "unit": "decimal ratio",
         "history": "20 consecutive valid turnover values", "statistic_ddof": "not applicable", "annualized": False,
         "direction": -1, "available_at": "after t close", "meaning": "average trading activity; denominator must be defined"},
    ])


def validate_math_and_edges() -> dict:
    """用独立小样本手算和边界条件检查定义，避免只验证程序能运行。"""
    dates = pd.bdate_range("2024-01-02", periods=25)
    rows = [{"symbol": symbol, "trade_date": d, "adj_close": base + i * step,
             "turnover_rate": 0.01 + i * 0.001, "in_universe": True}
            for symbol, base, step in [("A", 10.0, 0.05), ("B", 100.0, -0.1)]
            for i, d in enumerate(dates)]
    inputs = pd.DataFrame(rows)
    results = compute_factors(inputs, dates, ["A", "B"])
    stock = results[results.symbol.eq("A")].reset_index(drop=True)
    assert math.isclose(stock.loc[20, "mom20"], 0.10, abs_tol=1e-12)
    returns = [(10 + i * 0.05) / (10 + (i - 1) * 0.05) - 1 for i in range(1, 21)]
    avg = sum(returns) / len(returns)
    sample_std = math.sqrt(sum((r - avg) ** 2 for r in returns) / 19)
    assert math.isclose(stock.loc[20, "vol20"], sample_std, rel_tol=1e-10, abs_tol=1e-12)
    assert math.isclose(stock.loc[19, "turn20"], sum(0.01 + i * 0.001 for i in range(20)) / 20, abs_tol=1e-12)
    for _, group in results.groupby("symbol"):
        assert group.ret_1d.iloc[:1].isna().all()
        assert group.mom20.iloc[:20].isna().all() and pd.notna(group.mom20.iloc[20])
        assert group.vol20.iloc[:20].isna().all() and pd.notna(group.vol20.iloc[20])
        assert group.turn20.iloc[:19].isna().all() and pd.notna(group.turn20.iloc[19])
    # 缺一行后重新补全日历；动量端点虽有效，中间缺价仍使 mom20 缺失。
    gap = inputs.loc[~(inputs.symbol.eq("A") & inputs.trade_date.eq(dates[10]))]
    with_gap = compute_factors(gap, dates, ["A", "B"])
    ga = with_gap[with_gap.symbol.eq("A")].reset_index(drop=True)
    gb = with_gap[with_gap.symbol.eq("B")].reset_index(drop=True)
    assert ga.loc[[10, 11], "ret_1d"].isna().all()
    assert pd.isna(ga.loc[20, "mom20"]) and pd.isna(ga.loc[20, "vol20"])
    pd.testing.assert_series_equal(gb.mom20, results[results.symbol.eq("B")].mom20.reset_index(drop=True))
    base = pd.DataFrame({"symbol": ["A", "B", "C", "D", "E"], "trade_date": "2024-02-01",
                         "mom20": [0, 1, 2, 3, 100], "vol20": [1, 2, 3, 4, 5],
                         "turn20": [5, 4, 3, 2, 1], "in_universe": True})
    processed, audit = preprocess_factors(base)
    mom_audit = audit[audit.factor.eq("mom20")].iloc[0]
    assert mom_audit["median"] == 2 and mom_audit["mad"] == 1
    assert mom_audit["lower"] == -1 and mom_audit["upper"] == 5
    assert processed.mom20_clip.tolist() == [0, 1, 2, 3, 5]
    for factor in FACTORS:
        assert abs(processed[f"{factor}_z"].mean()) < 1e-12
        assert math.isclose(processed[f"{factor}_z"].std(ddof=0), 1, abs_tol=1e-12)
        pd.testing.assert_series_equal(processed[f"{factor}_score"],
            DIRECTIONS[factor] * processed[f"{factor}_z"], check_names=False)
    zero_mad = base.copy(); zero_mad["mom20"] = [1, 1, 1, 1, 10]
    kept, flags = preprocess_factors(zero_mad)
    assert kept.mom20_clip.tolist() == [1, 1, 1, 1, 10]
    assert flags.loc[flags.factor.eq("mom20"), "mad_zero"].all()
    constant = base.copy(); constant["mom20"] = 0.1
    constant_result, constant_audit = preprocess_factors(constant)
    assert constant_result.mom20_z.isna().all()
    assert constant_audit.loc[constant_audit.factor.eq("mom20"), "z_status"].eq("zero_std").all()
    too_small, too_small_audit = preprocess_factors(base.iloc[:4])
    assert too_small[[f"{f}_score" for f in FACTORS]].isna().all().all()
    assert too_small_audit.z_status.eq("insufficient_n").all()
    invalid_domain = base.copy()
    invalid_domain.loc[0, "vol20"] = -1
    invalid_domain.loc[1, "turn20"] = -1
    domain_result, _ = preprocess_factors(invalid_domain)
    assert not domain_result.loc[[0, 1], "common_valid"].any()
    assert domain_result.cross_section_n.eq(3).all()
    return {"manual_momentum_10_percent": True, "sample_std_ddof1": True,
            "turnover_mean_and_warmup": True, "stock_boundaries": True,
            "calendar_gap_propagation": True, "raw_mad_manual_example": True,
            "mad_zero_keeps_values": True, "zero_std_is_missing": True,
            "min_n_is_enforced": True, "zscore_mean0_std1": True,
            "fixed_directions": True, "negative_volatility_or_turnover_excluded": True}


def records(frame: pd.DataFrame) -> list[dict]:
    """转换为 JSON 记录，pandas 将 NaN 表示为真正的 null。"""
    return json.loads(frame.to_json(orient="records", force_ascii=False, double_precision=12))


def build_chart_data(raw: pd.DataFrame, processed: pd.DataFrame,
                     corr_raw: pd.DataFrame, corr_z: pd.DataFrame,
                     snapshot_date: str) -> dict:
    snapshot = processed[processed.trade_date.eq(snapshot_date) & processed.common_valid].sort_values("symbol")
    series = processed[processed.symbol.eq("SIM001")].sort_values("trade_date")
    return {
        "data_kind": DATA_KIND, "snapshot_date": snapshot_date,
        "calendar_note": "80 pandas business dates; NOT an A-share exchange calendar",
        "price_note": "fictional, no corporate actions; adj_close equals raw price",
        "turnover_unit": "decimal (0.025 = 2.5%)", "volatility_ddof": 1,
        "mad_convention": "raw median absolute deviation; bounds median +/- 3*MAD; no 1.4826 scaling",
        "zscore_ddof": 0, "min_n": MIN_N, "directions": DIRECTIONS,
        "symbols": snapshot.symbol.tolist(), "factor_names": FACTORS,
        "snapshot": records(snapshot[KEY + FACTORS + [f"{f}_{s}" for f in FACTORS for s in ("clip", "z", "score")]]),
        "momentum_series": records(series[["trade_date", "adj_close", "ret_1d", "mom20", "vol20", "turn20"]]),
        "distributions": {f: {"symbols": snapshot.symbol.tolist(), "raw": snapshot[f].tolist(),
            "clipped": snapshot[f"{f}_clip"].tolist(), "z": snapshot[f"{f}_z"].tolist()} for f in FACTORS},
        "correlation": {"n_common": len(snapshot), "labels": FACTORS,
            "raw": json.loads(corr_raw.to_json(orient="values", double_precision=12)),
            "z": json.loads(corr_z.to_json(orient="values", double_precision=12))},
        "input_rows": len(raw), "grid_rows": len(processed),
    }


def run(output: Path) -> dict:
    """写入专属实验目录；其他非空目录会被拒绝，重跑不追加数据。"""
    output = output.resolve()
    marker = output / ".quant_babies_lecture03_simulation"
    if output.exists() and not output.is_dir():
        raise FileExistsError(f"Output is not a directory: {output}")
    if output.exists() and any(output.iterdir()) and not marker.exists():
        raise FileExistsError(f"Refusing to overwrite a non-lab directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    marker.write_text("Simulation output only. No real market data.\n", encoding="utf-8")
    raw, calendar = make_teaching_data()
    raw.to_csv(output / "raw_simulated.csv", index=False)
    pd.DataFrame({"trade_date": calendar.strftime("%Y-%m-%d"), "is_simulated_session": True}).to_csv(
        output / "calendar_simulated.csv", index=False)
    # 从 CSV 重读，模拟真实项目的类型入口；代码不能当整数解析。
    loaded = pd.read_csv(output / "raw_simulated.csv", dtype={"symbol": "string", "trade_date": "string"})
    factors = compute_factors(loaded, calendar, UNIVERSE)
    processed, audit = preprocess_factors(factors)
    factors.to_csv(output / "factors_raw.csv", index=False)
    processed.to_csv(output / "factors_processed.csv", index=False)
    audit.to_csv(output / "preprocessing_audit.csv", index=False)
    factor_definitions().to_csv(output / "factor_definitions.csv", index=False)
    snapshot_date = str(calendar[-1].date())  # 固定设计为最后一个模拟日期，不搜索最漂亮的截面。
    snapshot = processed[processed.trade_date.eq(snapshot_date) & processed.common_valid].sort_values("symbol")
    corr_raw = snapshot[FACTORS].corr(method="pearson", min_periods=MIN_N)
    corr_z = snapshot[[f"{f}_z" for f in FACTORS]].rename(columns={f"{f}_z": f for f in FACTORS}).corr(
        method="pearson", min_periods=MIN_N)
    corr_raw.to_csv(output / "correlation_raw.csv", index_label="factor")
    corr_z.to_csv(output / "correlation_z.csv", index_label="factor")
    checks = validate_math_and_edges()
    # 扰动最后五个日期，过去所有原始因子和横截面处理结果必须原样不变。
    cutoff = str(calendar[-5].date())
    perturbed = loaded.copy()
    future = perturbed.trade_date.ge(cutoff)
    perturbed.loc[future, "adj_close"] *= 1.2
    perturbed.loc[future, "turnover_rate"] *= 1.7
    future_factors = compute_factors(perturbed, calendar, UNIVERSE)
    future_processed, _ = preprocess_factors(future_factors)
    selected = KEY + FACTORS + [f"{f}_{s}" for f in FACTORS for s in ("clip", "z", "score")]
    pd.testing.assert_frame_equal(processed.loc[processed.trade_date.lt(cutoff), selected].reset_index(drop=True),
        future_processed.loc[future_processed.trade_date.lt(cutoff), selected].reset_index(drop=True))
    checks["future_perturbation_preserves_past"] = True
    checks["unique_complete_calendar_grid"] = len(factors) == len(UNIVERSE) * len(calendar) and not factors.duplicated(KEY).any()
    checks["no_backfill_or_zero_fill"] = bool(factors.adj_close.isna().sum() == 3)
    checks["snapshot_has_eight_common_stocks"] = len(snapshot) == 8
    assert all(checks.values())
    charts = build_chart_data(raw, processed, corr_raw, corr_z, snapshot_date)
    (output / "chart_data.json").write_text(json.dumps(charts, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    report = {
        "data_kind": DATA_KIND, "calendar": "80 pandas business dates; NOT an exchange trading calendar",
        "n_symbols": len(UNIVERSE), "input_rows": len(raw), "grid_rows": len(factors),
        "missing_grid_rows_added": len(factors) - len(raw), "missing_prices": int(factors.adj_close.isna().sum()),
        "unknown_turnover_rows": int(factors.turnover_rate.isna().sum()),
        "snapshot_date": snapshot_date, "snapshot_common_n": len(snapshot),
        "common_sample_policy": "all three factors finite, in predeclared universe, same trade_date",
        "mad_k": MAD_K, "mad_scaled_by_1_4826": False, "mad_zero_policy": "keep raw and flag",
        "min_n": MIN_N, "volatility_ddof": 1, "zscore_ddof": 0, "volatility_annualized": False,
        "directions": DIRECTIONS, "direction_note": "teaching hypotheses, never fitted to future returns",
        "pandas_version": pd.__version__, "checks": checks,
        "factor_nonmissing_rows": {f: int(factors[f].notna().sum()) for f in FACTORS},
        "preprocessing_counts": audit.z_status.value_counts().to_dict(),
        "input_sha256": hashlib.sha256((output / "raw_simulated.csv").read_bytes()).hexdigest(),
    }
    (output / "quality_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Lecture 03: offline simulated factor engineering; no real A-share or strategy results.")
    parser.add_argument("--output", type=Path, default=Path("data/processed/lecture-03-simulation"),
                        help="Dedicated simulation output directory; unrelated nonempty directories are refused.")
    args = parser.parse_args()
    try:
        report = run(args.output)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"Factor lab failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"data_kind": DATA_KIND, "input_rows": report["input_rows"], "grid_rows": report["grid_rows"],
        "snapshot_date": report["snapshot_date"], "snapshot_common_n": report["snapshot_common_n"],
        "checks": report["checks"], "output": str(args.output.resolve())}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
