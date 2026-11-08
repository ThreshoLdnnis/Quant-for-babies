"""番外期第二讲：可离线复现的模拟金融数据工程实验。

SIM001 / SIM002 均为虚构证券；日期只是工作日序列，不是 A 股交易日历。
本脚本不联网、不产生真实 A 股结果，也不构成投资策略。
"""

from __future__ import annotations

import argparse
from contextlib import closing
import json
import math
from pathlib import Path
import sqlite3
import sys

import pandas as pd


NUMERIC = ["open", "high", "low", "close", "volume", "amount"]
KEY = ["symbol", "trade_date"]
RAW_COLUMNS = KEY + NUMERIC + ["adjustment", "source", "is_simulated"]

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE securities (
  symbol TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  industry TEXT NOT NULL
);
CREATE TABLE prices (
  symbol TEXT NOT NULL REFERENCES securities(symbol),
  trade_date TEXT NOT NULL CHECK(length(trade_date) = 10),
  open REAL NOT NULL CHECK(open > 0),
  high REAL NOT NULL CHECK(high >= open AND high >= close AND high >= low),
  low REAL NOT NULL CHECK(low > 0 AND low <= open AND low <= close),
  close REAL NOT NULL CHECK(close > 0),
  volume INTEGER NOT NULL CHECK(volume >= 0),
  amount REAL NOT NULL CHECK(amount >= 0),
  adjustment TEXT NOT NULL CHECK(adjustment = 'raw'),
  source TEXT NOT NULL,
  is_simulated INTEGER NOT NULL CHECK(is_simulated = 1),
  PRIMARY KEY(symbol, trade_date)
);
CREATE INDEX idx_prices_date ON prices(trade_date);
"""

QUERIES = {
    "select": """SELECT symbol, trade_date, close, volume
FROM prices
WHERE symbol = 'SIM001' AND trade_date >= '2024-01-10'
ORDER BY trade_date
LIMIT 5;""",
    "aggregate": """SELECT symbol, COUNT(*) AS n_bars,
       AVG(close) AS avg_close, SUM(amount) AS total_amount
FROM prices
GROUP BY symbol
ORDER BY symbol;""",
    "left_join": """SELECT s.symbol, s.name, COUNT(q.trade_date) AS n_bars
FROM securities AS s
LEFT JOIN prices AS q
  ON s.symbol = q.symbol AND q.trade_date >= '2024-01-01'
GROUP BY s.symbol, s.name
ORDER BY s.symbol;""",
    "lag": """WITH previous AS (
  SELECT symbol, trade_date, close,
         LAG(close) OVER (
           PARTITION BY symbol ORDER BY trade_date
         ) AS prev_close
  FROM prices
)
SELECT symbol, trade_date, close, prev_close,
       1.0 * close / NULLIF(prev_close, 0) - 1 AS return_observed
FROM previous
ORDER BY symbol, trade_date;""",
    "latest": """WITH ranked AS (
  SELECT symbol, trade_date, close,
         ROW_NUMBER() OVER (
           PARTITION BY symbol ORDER BY trade_date DESC
         ) AS rn
  FROM prices
)
SELECT symbol, trade_date, close
FROM ranked WHERE rn = 1
ORDER BY symbol;""",
}


def make_raw() -> tuple[pd.DataFrame, pd.DatetimeIndex]:
    """产生固定数据，并刻意注入可核对的数据质量问题。"""
    dates = pd.bdate_range("2024-01-02", periods=40)
    rows = []
    for stock_no, symbol in enumerate(["SIM001", "SIM002"]):
        for i, date in enumerate(dates):
            # SIM002 第 11 个模拟工作日假设停牌：不伪造一根成交 K 线。
            if symbol == "SIM002" and i == 10:
                continue
            close = round(10 + stock_no * 10 + i * 0.06 + (i % 5 - 2) * 0.03, 2)
            opening = round(close + (0.02 if i % 2 else -0.02), 2)
            volume = 10000 + stock_no * 2000 + i * 100
            rows.append({
                "symbol": symbol, "trade_date": date.strftime("%Y-%m-%d"),
                "open": opening, "high": round(max(opening, close) + 0.10, 2),
                "low": round(min(opening, close) - 0.10, 2), "close": close,
                "volume": volume, "amount": round(close * volume, 2),
                "adjustment": "raw", "source": "deterministic_simulation",
                "is_simulated": 1,
            })
    raw = pd.DataFrame(rows, columns=RAW_COLUMNS)
    raw["close"] = raw["close"].astype("object")
    raw.loc[(raw.symbol == "SIM001") & (raw.trade_date == str(dates[12].date())), "close"] = None
    raw.loc[(raw.symbol == "SIM001") & (raw.trade_date == str(dates[13].date())), "high"] = 1.0
    raw.loc[(raw.symbol == "SIM001") & (raw.trade_date == str(dates[14].date())), "volume"] = -100
    raw.loc[(raw.symbol == "SIM002") & (raw.trade_date == str(dates[15].date())), "trade_date"] = "not-a-date"
    raw.loc[(raw.symbol == "SIM002") & (raw.trade_date == str(dates[16].date())), "close"] = "oops"
    exact = raw[(raw.symbol == "SIM001") & (raw.trade_date == str(dates[5].date()))].copy()
    conflict = raw[(raw.symbol == "SIM001") & (raw.trade_date == str(dates[7].date()))].copy()
    conflict["volume"] += 17
    raw = pd.concat([raw, exact, conflict], ignore_index=True)
    raw = raw.sample(frac=1, random_state=42).reset_index(drop=True)
    raw.insert(0, "raw_row_id", range(1, len(raw) + 1))
    return raw, dates


def clean_prices(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """完全重复仅留一个；冲突键全部隔离；其他错误逐条记录原因。"""
    exact_mask = raw.duplicated(subset=RAW_COLUMNS, keep="first")
    exact = raw.loc[exact_mask].copy()
    exact["issue"] = "exact_duplicate"
    work = raw.loc[~exact_mask].copy()
    work["trade_date"] = pd.to_datetime(work["trade_date"], format="%Y-%m-%d", errors="coerce")
    for col in NUMERIC:
        work[col] = pd.to_numeric(work[col], errors="coerce")
    # 有效日期才可构成业务键；无效日期稍后单独隔离。
    conflict_mask = work.trade_date.notna() & work.duplicated(KEY, keep=False)
    conflicting = work.loc[conflict_mask].copy()
    conflicting["issue"] = "conflicting_duplicate_key"
    work = work.loc[~conflict_mask].copy()
    issues = pd.Series("", index=work.index, dtype="object")

    def mark(mask: pd.Series, reason: str) -> None:
        issues.loc[mask] = issues.loc[mask] + reason + ";"

    mark(work.trade_date.isna(), "invalid_date")
    mark(work[NUMERIC].isna().any(axis=1), "missing_or_non_numeric")
    mark(work[NUMERIC].apply(lambda s: s.map(lambda x: not math.isfinite(x))).any(axis=1), "nonfinite_numeric")
    mark((work[["open", "high", "low", "close"]] <= 0).any(axis=1), "nonpositive_price")
    mark((work.high < work[["open", "close", "low"]].max(axis=1)) |
         (work.low > work[["open", "close"]].min(axis=1)), "invalid_ohlc")
    mark((work.volume < 0) | (work.amount < 0), "negative_activity")
    mark(work.volume.notna() & (work.volume % 1 != 0), "fractional_volume")
    bad = work.loc[issues != ""].copy()
    bad["issue"] = issues.loc[issues != ""].str.rstrip(";")
    clean = work.loc[issues == "", RAW_COLUMNS].copy()
    clean = clean.sort_values(KEY).reset_index(drop=True)
    clean["volume"] = clean.volume.astype("int64")
    clean["trade_date"] = clean.trade_date.dt.strftime("%Y-%m-%d")
    quarantine = pd.concat([exact, conflicting, bad], ignore_index=True)
    quarantine = quarantine.sort_values("raw_row_id").reset_index(drop=True)
    # 原始文件保留字符串原貌；隔离文件展示规范化值并保留可追溯行号。
    report = {
        "data_kind": "SIMULATION_ONLY_NOT_REAL_A_SHARE_RESULTS",
        "calendar": "40 pandas business dates; NOT an exchange trading calendar",
        "raw_rows": len(raw), "exact_duplicate_rows_removed": len(exact),
        "conflicting_duplicate_rows_quarantined": len(conflicting),
        "invalid_rows_quarantined": len(bad), "clean_rows": len(clean),
        "quarantine_rows": len(quarantine),
        "missing_value_policy": "quarantine; never forward-fill prices or label missing bars as suspension",
        "price_basis": "raw simulation; no corporate action in this fictional dataset",
    }
    assert len(raw) == len(clean) + len(quarantine)
    assert not clean.duplicated(KEY).any()
    return clean, quarantine, report


def add_features(clean: pd.DataFrame) -> pd.DataFrame:
    """窗口基于每只股票的有效观测行；有缺口时不冒充每日收益。"""
    features = clean.sort_values(KEY).copy()
    grouped = features.groupby("symbol", sort=False)
    features["prev_date"] = grouped["trade_date"].shift(1)
    features["prev_close"] = grouped["close"].shift(1)
    features["return_observed"] = features.close / features.prev_close - 1
    features["momentum_20obs"] = features.close / grouped["close"].shift(20) - 1
    features["ma5"] = grouped["close"].transform(lambda s: s.rolling(5, min_periods=5).mean())
    features["ma20"] = grouped["close"].transform(lambda s: s.rolling(20, min_periods=20).mean())
    # 收盘后才知道当日均线；向后移动一行，示范下一有效观测行才可用的特征。
    features["ma5_prev_observation"] = features.groupby("symbol")["ma5"].shift(1)
    features["gap_days"] = (pd.to_datetime(features.trade_date) - pd.to_datetime(features.prev_date)).dt.days
    return features


def validate_features(clean: pd.DataFrame, features: pd.DataFrame) -> dict:
    """检查暖机边界，并通过扰动未来输入检查过去特征是否改变。"""
    for _, stock in features.groupby("symbol", sort=False):
        for window in (5, 20):
            values = stock[f"ma{window}"]
            assert values.iloc[:window - 1].isna().all()
            if len(values) >= window:
                assert pd.notna(values.iloc[window - 1])
        assert stock["momentum_20obs"].iloc[:20].isna().all()
        if len(stock) >= 21:
            assert pd.notna(stock["momentum_20obs"].iloc[20])

    changed = clean.sort_values(KEY).copy()
    position = changed.groupby("symbol").cumcount()
    size = changed.groupby("symbol")["close"].transform("size")
    future_rows = position >= size - 5
    # 只改每只证券最后五行。之前的任何特征都不应该读取这些未来价格。
    changed.loc[future_rows, ["open", "high", "low", "close", "amount"]] *= 1.37
    recalculated = add_features(changed)
    feature_columns = ["prev_date", "prev_close", "return_observed", "momentum_20obs",
                       "ma5", "ma20", "ma5_prev_observation", "gap_days"]
    pd.testing.assert_frame_equal(
        features.loc[~future_rows, KEY + feature_columns].reset_index(drop=True),
        recalculated.loc[~future_rows, KEY + feature_columns].reset_index(drop=True),
        atol=1e-12, rtol=1e-12,
    )
    return {"ma5_warmup_boundary": True, "ma20_warmup_boundary": True,
            "momentum20_warmup_boundary": True, "future_perturbation_preserves_past_features": True}


def build_database(path: Path, clean: pd.DataFrame) -> dict:
    if sqlite3.sqlite_version_info < (3, 25, 0):
        raise RuntimeError("SQLite >= 3.25.0 is required for window functions")
    # 路径位于本实验专属目录；事务内重建表，重复运行得到同一数据，不追加重复行。
    with closing(sqlite3.connect(path)) as connection, connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("DROP TABLE IF EXISTS prices")
        connection.execute("DROP TABLE IF EXISTS securities")
        connection.executescript(SCHEMA)
        connection.executemany("INSERT INTO securities VALUES (?, ?, ?)", [
            ("SIM001", "模拟甲", "模拟制造"),
            ("SIM002", "模拟乙", "模拟金融"),
            ("SIM003", "模拟待研究证券（无行情）", "模拟服务"),
        ])
        placeholders = ",".join("?" for _ in RAW_COLUMNS)
        insert = f"INSERT INTO prices ({','.join(RAW_COLUMNS)}) VALUES ({placeholders})"
        connection.executemany(insert, clean[RAW_COLUMNS].itertuples(index=False, name=None))
        check = connection.execute("PRAGMA integrity_check").fetchone()[0]
        assert check == "ok", check
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
        outputs = {}
        for name, query in QUERIES.items():
            result = pd.read_sql_query(query, connection)
            outputs[name] = json.loads(result.to_json(orient="records", force_ascii=False))
        lag = pd.read_sql_query(QUERIES["lag"], connection)
        pandas_features = add_features(clean)
        # 先按业务键一对一对齐；不能仅凭两张表碰巧具有相同的行顺序。
        aligned = pandas_features[KEY + ["close", "prev_close", "return_observed"]].merge(
            lag, on=KEY, how="outer", validate="one_to_one", indicator=True,
            suffixes=("_pd", "_sql"),
        )
        assert aligned["_merge"].eq("both").all()
        for column in ("close", "prev_close", "return_observed"):
            left, right = aligned[f"{column}_pd"], aligned[f"{column}_sql"]
            assert left.isna().equals(right.isna()), f"NULL mismatch: {column}"
            valid = left.notna()
            pd.testing.assert_series_equal(left[valid], right[valid], check_names=False,
                                           check_dtype=False, atol=1e-12, rtol=1e-12)
        assert outputs["left_join"][-1]["n_bars"] == 0
        return outputs


def run(output: Path) -> dict:
    """只在专属子目录中读写实验生成物，拒绝覆盖不属于本实验的现存目录。"""
    output = output.resolve()
    marker = output / ".quant_babies_lecture02_simulation"
    if output.exists() and any(output.iterdir()) and not marker.exists():
        raise FileExistsError(f"Refusing to overwrite a non-lab directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    marker.write_text("Generated simulation files only. No real market data.\n", encoding="utf-8")
    raw, dates = make_raw()
    raw.to_csv(output / "raw_simulated.csv", index=False, encoding="utf-8")
    # 用 CSV 往返模拟日常读取。证券代码必须为字符串，避免前导零丢失。
    loaded = pd.read_csv(output / "raw_simulated.csv", dtype={"symbol": "string", "trade_date": "string"})
    clean, quarantine, report = clean_prices(loaded)
    features = add_features(clean)
    feature_checks = validate_features(clean, features)
    clean.to_csv(output / "clean_simulated.csv", index=False, encoding="utf-8")
    quarantine.to_csv(output / "quarantine_simulated.csv", index=False, encoding="utf-8")
    features.to_csv(output / "features_simulated.csv", index=False, encoding="utf-8")
    expected = pd.MultiIndex.from_product([["SIM001", "SIM002"], dates.strftime("%Y-%m-%d")], names=KEY)
    observed = pd.MultiIndex.from_frame(clean[KEY])
    missing = expected.difference(observed)
    report["missing_expected_keys"] = [{"symbol": s, "trade_date": d,
        "status": "simulated_suspension" if s == "SIM002" and d == dates[10].strftime("%Y-%m-%d")
                  else "unresolved_data_gap"} for s, d in missing]
    report["sqlite_version"] = sqlite3.sqlite_version
    report["pandas_version"] = pd.__version__
    report["pandas_sql_return_match"] = True
    sql_results = build_database(output / "research_simulated.sqlite", clean)
    report["checks"] = {
        "unique_symbol_date": not clean.duplicated(KEY).any(),
        "no_missing_required_fields": not clean[RAW_COLUMNS].isna().any().any(),
        "sorted_by_symbol_date": clean[KEY].equals(clean.sort_values(KEY)[KEY]),
        "per_stock_first_return_is_missing": bool(features.groupby("symbol")["return_observed"].nth(0).isna().all()),
        "row_accounting": len(raw) == len(clean) + len(quarantine),
        "pandas_sql_keys_nulls_values_match": True,
        **feature_checks,
    }
    assert all(report["checks"].values())
    (output / "quality_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "sql_results.json").write_text(json.dumps(sql_results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "queries.sql").write_text("-- SIMULATED DATA ONLY\n\n" + "\n\n".join(
        f"-- {name}\n{query}" for name, query in QUERIES.items()), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline simulated financial data engineering lab (no real A-share results).")
    parser.add_argument("--output", type=Path, default=Path("data/processed/lecture-02-simulation"),
                        help="Dedicated lab output directory; non-lab nonempty directories are refused.")
    args = parser.parse_args()
    try:
        report = run(args.output)
    except (OSError, RuntimeError, sqlite3.Error) as exc:
        print(f"Lab failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"data_kind": report["data_kind"], "raw_rows": report["raw_rows"],
        "clean_rows": report["clean_rows"], "quarantine_rows": report["quarantine_rows"],
        "checks": report["checks"], "output": str(args.output.resolve())}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
