"""Lecture 05: a small, deterministic SIMULATED share-and-cash backtest.

No real A-share returns, current market fee schedule, or investable conclusion.
The unchanged lecture 03 data have no corporate actions: close_raw == adj_close.
Synthetic opening quotes use only the preceding raw close. Factor inputs are never filled.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

import pandas as pd

DATA_KIND = "SIMULATION_ONLY_NOT_REAL_A_SHARE_RESULTS"
STRATEGIES = ["mom20", "vol20", "turn20", "multi", "reference"]
INITIAL_CASH = 1_000_000.0
LOT_SIZE = 100  # Teaching convention, not a universal rule for every A-share board.
TOP_N = 3  # Eight-stock classroom example; a formal Top10 needs a larger universe.
# Fictional assumptions, not a quote of any historical/current market fee schedule.
COSTS = {
    "zero": {"commission": 0.0, "sell_tax": 0.0, "slippage": 0.0},
    "base": {"commission": 0.0003, "sell_tax": 0.0005, "slippage": 0.0005},
    "high": {"commission": 0.0006, "sell_tax": 0.0010, "slippage": 0.0010},
}


def load_factor_module():
    folder = Path(__file__).resolve().parent
    for path in [folder / "factor_lab.py", folder.parent / "lecture-03" / "factor_lab.py"]:
        if path.is_file():
            spec = importlib.util.spec_from_file_location("lecture03_factor_source", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module, path
    raise FileNotFoundError("Place unchanged lecture 03 factor_lab.py beside this script, or keep repository folders")


def records(frame: pd.DataFrame) -> list[dict]:
    return json.loads(frame.to_json(orient="records", force_ascii=False, double_precision=12))


def build_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DatetimeIndex, dict]:
    module, path = load_factor_module()
    raw, calendar = module.make_teaching_data()
    factors = module.compute_factors(raw, calendar, module.UNIVERSE)
    processed, _ = module.preprocess_factors(factors)
    processed["multi_score"] = processed[[f"{f}_score" for f in module.FACTORS]].mean(axis=1, skipna=False)
    market = make_execution_market(factors, calendar, module.UNIVERSE)
    provenance = {"factor_source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                  "raw_generator_csv_sha256": hashlib.sha256(raw.to_csv(index=False).encode("utf-8")).hexdigest(),
                  "input_rows": len(raw), "grid_rows": len(processed),
                  "directions": module.DIRECTIONS, "factor_source": "unchanged lecture 03 module"}
    return processed, market, calendar, provenance


def make_execution_market(factors: pd.DataFrame, calendar: pd.DatetimeIndex,
                          universe: list[str]) -> pd.DataFrame:
    """Add explicitly synthetic execution quotes; never use current/future close.

    open[t] = close_raw[t-1] * (1 + 0.001*sin(0.37*t + stock_index)).
    A missing preceding close yields a missing opening quote; there is no quote fill.
    Intraday close remains the unchanged original raw quote, including missing values.
    """
    market = factors[["symbol", "trade_date", "close_raw", "status"]].copy()
    market = market.sort_values(["symbol", "trade_date"]).reset_index(drop=True)
    position = {str(date.date()): i for i, date in enumerate(calendar)}
    stock_no = {symbol: i for i, symbol in enumerate(universe)}
    previous = market.groupby("symbol", sort=False)["close_raw"].shift(1)
    perturbation = market.apply(lambda r: 0.001 * math.sin(0.37 * position[r.trade_date] + stock_no[r.symbol]), axis=1)
    market["open_quote"] = previous * (1 + perturbation)
    market["known_full_day_suspension"] = market.status.eq("known_simulated_suspension")
    market.loc[market.known_full_day_suspension, "open_quote"] = float("nan")
    market["open_auction_halt"] = False
    market["buy_blocked"] = False
    market["sell_blocked"] = False
    # Predeclared teaching fixtures, unrelated to future realized returns.
    market.loc[market.symbol.eq("SIM004") & market.trade_date.eq(str(calendar[22].date())), "open_auction_halt"] = True
    market.loc[market.symbol.eq("SIM007") & market.trade_date.eq(str(calendar[22].date())), "buy_blocked"] = True
    market.loc[market.symbol.eq("SIM001") & market.trade_date.eq(str(calendar[43].date())), "sell_blocked"] = True
    market["is_simulated"] = True
    return market


def make_schedule(calendar: pd.DatetimeIndex) -> pd.DataFrame:
    """Use the final grid day of completed simulated months; append terminal audit only."""
    rows = []
    for index, date in enumerate(calendar):
        next_date = calendar[index + 1] if index + 1 < len(calendar) else None
        month_changes = next_date is not None and next_date.to_period("M") != date.to_period("M")
        if month_changes:
            rows.append({"signal_date": str(date.date()), "execution_date": str(next_date.date()),
                         "signal_kind": "completed_grid_month", "status": "scheduled_next_open"})
        elif index == len(calendar) - 1:
            rows.append({"signal_date": str(date.date()), "execution_date": None,
                         "signal_kind": "terminal_partial_month_audit", "status": "terminal_no_next_open"})
    return pd.DataFrame(rows)


def build_signals(processed: pd.DataFrame, schedule: pd.DataFrame,
                  universe: list[str], top_n: int = TOP_N) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Freeze each close-time target independently of future labels and execution prices."""
    scores, targets = [], []
    score_columns = ["mom20_score", "vol20_score", "turn20_score"]
    for event in schedule.to_dict("records"):
        date = event["signal_date"]
        section = processed[processed.trade_date.eq(date)].copy()
        eligible = section[section[score_columns].notna().all(axis=1)].copy()
        for strategy in STRATEGIES:
            if strategy == "reference":
                selected = list(universe)
                ranked = None
            else:
                score = "multi_score" if strategy == "multi" else f"{strategy}_score"
                ranked = eligible.sort_values([score, "symbol"], ascending=[False, True], kind="stable")
                # The code-based tie-break is declared beforehand; no return information.
                selected = ranked.symbol.iloc[:top_n].tolist() if len(ranked) >= top_n else []
                for rank, row in enumerate(ranked.to_dict("records"), 1):
                    scores.append({"signal_date": date, "execution_date": event["execution_date"],
                                   "strategy": strategy, "symbol": row["symbol"], "rank": rank,
                                   "score": row[score], "selected": row["symbol"] in selected,
                                   "n_eligible": len(ranked), "tie_break": "symbol ascending"})
            for symbol in universe:
                weight = 1 / len(selected) if symbol in selected else 0.0
                targets.append({"signal_date": date, "execution_date": event["execution_date"],
                                "signal_kind": event["signal_kind"], "strategy": strategy,
                                "symbol": symbol, "target_weight": weight,
                                "n_eligible": len(universe) if strategy == "reference" else len(eligible),
                                "target_status": "formed" if selected else "insufficient_candidates_cash_target"})
    return pd.DataFrame(scores), pd.DataFrame(targets)


def metric_summary(daily: pd.DataFrame) -> dict:
    """Descriptive daily metrics, annualization as a short-sample approximation only."""
    values = daily.daily_return.replace([float("inf"), float("-inf")], float("nan")).dropna()
    n = len(values)
    total = float(daily.nav.iloc[-1] - 1) if len(daily) else float("nan")
    annual = (1 + total) ** (252 / n) - 1 if n and 1 + total > 0 else float("nan")
    sd = 0.0 if n >= 2 and values.nunique() <= 1 else (float(values.std(ddof=1)) if n >= 2 else float("nan"))
    vol = sd * math.sqrt(252) if math.isfinite(sd) else float("nan")
    sharpe = math.sqrt(252) * float(values.mean()) / sd if n >= 2 and math.isfinite(sd) and sd > 0 else float("nan")
    return {"n_periods": n, "total_return": total, "annualized_return": annual,
            "annualized_vol": vol, "sharpe": sharpe,
            "max_drawdown": float(daily.drawdown.min()) if len(daily) else float("nan"),
            "annualization_days": 252, "daily_risk_free": 0.0, "sample_sd_ddof": 1,
            "metric_note": "80 simulated periods including cash warmup; short sample, not an OOS claim"}


def order_block(row: dict, side: str) -> str | None:
    if row["known_full_day_suspension"]:
        return "known_simulated_full_day_suspension"
    if row["open_auction_halt"]:
        return "synthetic_open_auction_halt"
    if row[f"{side}_blocked"]:
        return f"synthetic_{side}_blocked"
    if pd.isna(row["open_quote"]) or not math.isfinite(row["open_quote"]) or row["open_quote"] <= 0:
        return "missing_open_quote"
    return None


def simulate(market: pd.DataFrame, targets: pd.DataFrame, calendar: pd.DatetimeIndex,
             universe: list[str], strategy: str = "multi", scenario: str = "base",
             initial_cash: float = INITIAL_CASH, lot_size: int = LOT_SIZE) -> dict[str, pd.DataFrame | dict]:
    """One opening event per date, prior holdings sold first, then cash-limited buys.

    Target share quantities are rounded down using pretrade opening equity and mid quotes.
    Cash-limited purchases follow a predeclared symbol order, so fills can underweight targets.
    An unfilled order expires at that opening; it is not silently filled on another day.
    """
    if strategy not in STRATEGIES or scenario not in COSTS or initial_cash <= 0 or lot_size <= 0:
        raise ValueError("Invalid strategy, cost scenario, cash or lot size")
    costs = COSTS[scenario]
    selected_targets = targets[targets.strategy.eq(strategy) & targets.execution_date.notna()]
    events = {date: group.set_index("symbol").to_dict("index") for date, group in selected_targets.groupby("execution_date")}
    market_by_date = {date: group.set_index("symbol").to_dict("index") for date, group in market.groupby("trade_date")}
    shares = {symbol: 0 for symbol in universe}
    last_marks = {symbol: float("nan") for symbol in universe}
    cash, previous_equity, running_peak = float(initial_cash), float(initial_cash), float(initial_cash)
    daily_rows, holdings, orders, trades, weights = [], [], [], [], []
    for date_obj in calendar:
        date = str(date_obj.date())
        quotes = market_by_date[date]
        start_shares = shares.copy()
        open_marks = {symbol: (quotes[symbol]["open_quote"] if pd.notna(quotes[symbol]["open_quote"]) else last_marks[symbol]) for symbol in universe}
        for symbol in universe:
            if shares[symbol] and (pd.isna(open_marks[symbol]) or open_marks[symbol] <= 0):
                raise ValueError("An existing holding has no defensible opening valuation")
        pretrade_equity = cash + sum(shares[s] * open_marks[s] for s in universe if shares[s])
        commission_day = tax_day = slippage_day = turnover_notional = 0.0
        if date in events:
            event = events[date]
            before_qty = shares.copy()
            before_cash = cash
            before_weights = {s: shares[s] * open_marks[s] / pretrade_equity if shares[s] else 0.0 for s in universe}
            target_quantities = {}
            for symbol in universe:
                weight = event[symbol]["target_weight"]
                quote = quotes[symbol]["open_quote"]
                if weight == 0:
                    target_quantities[symbol] = 0
                elif pd.notna(quote) and quote > 0:
                    target_quantities[symbol] = math.floor(pretrade_equity * weight / quote / lot_size) * lot_size
                else:
                    target_quantities[symbol] = shares[symbol]
                    orders.append({"trade_date": date, "signal_date": event[symbol]["signal_date"], "symbol": symbol,
                                   "side": "target", "requested_quantity": None, "filled_quantity": 0,
                                   "status": "missing_open_quote_target_uncomputable"})
            for side in ("sell", "buy"):
                for symbol in sorted(universe):
                    difference = target_quantities[symbol] - shares[symbol]
                    requested = -difference if side == "sell" and difference < 0 else difference if side == "buy" and difference > 0 else 0
                    if requested == 0:
                        continue
                    blocked = order_block(quotes[symbol], side)
                    filled, status = 0, blocked
                    if blocked is None:
                        quote = float(quotes[symbol]["open_quote"])
                        execution_price = quote * (1 - costs["slippage"] if side == "sell" else 1 + costs["slippage"])
                        if side == "sell":
                            filled = min(requested, start_shares[symbol])
                        else:
                            affordable = max(0, math.floor((cash + 1e-9) / (execution_price * (1 + costs["commission"])) / lot_size) * lot_size)
                            filled = min(requested, affordable)
                        status = "filled" if filled == requested else "partial_cash_limit" if filled else "cash_below_one_lot"
                        if filled:
                            executed_notional = filled * execution_price
                            commission = executed_notional * costs["commission"]
                            sell_tax = executed_notional * costs["sell_tax"] if side == "sell" else 0.0
                            slippage = filled * abs(execution_price - quote)
                            cash += executed_notional - commission - sell_tax if side == "sell" else -executed_notional - commission
                            shares[symbol] += -filled if side == "sell" else filled
                            commission_day += commission
                            tax_day += sell_tax
                            slippage_day += slippage
                            turnover_notional += filled * quote
                            trades.append({"trade_date": date, "signal_date": event[symbol]["signal_date"],
                                           "symbol": symbol, "side": side, "quantity": filled, "open_quote": quote,
                                           "execution_price": execution_price, "executed_notional": executed_notional,
                                           "commission": commission, "sell_tax": sell_tax, "slippage_cost": slippage,
                                           "cash_after": cash})
                    orders.append({"trade_date": date, "signal_date": event[symbol]["signal_date"], "symbol": symbol,
                                   "side": side, "requested_quantity": requested, "filled_quantity": filled, "status": status})
            after_equity = cash + sum(shares[s] * open_marks[s] for s in universe if shares[s])
            for symbol in universe:
                weights.append({"trade_date": date, "signal_date": event[symbol]["signal_date"], "symbol": symbol,
                                "before_weight": before_weights[symbol], "target_weight": event[symbol]["target_weight"],
                                "after_weight": shares[symbol] * open_marks[symbol] / after_equity if shares[symbol] else 0.0,
                                "before_quantity": before_qty[symbol], "after_quantity": shares[symbol],
                                "pretrade_equity": pretrade_equity, "after_trade_equity": after_equity})
            weights.append({"trade_date": date, "signal_date": next(iter(event.values()))["signal_date"], "symbol": "CASH",
                            "before_weight": before_cash / pretrade_equity,
                            "target_weight": max(0.0, 1 - sum(event[s]["target_weight"] for s in universe)),
                            "after_weight": cash / after_equity, "before_quantity": None, "after_quantity": None,
                            "pretrade_equity": pretrade_equity, "after_trade_equity": after_equity})
        stale_held_count = 0
        holding_value = 0.0
        for symbol in universe:
            close = quotes[symbol]["close_raw"]
            stale = pd.isna(close)
            if not stale:
                last_marks[symbol] = float(close)
            mark = last_marks[symbol]
            if shares[symbol] and (pd.isna(mark) or mark <= 0):
                raise ValueError("Holding lacks a usable valuation mark")
            value = shares[symbol] * mark if shares[symbol] else 0.0
            holding_value += value
            stale_held_count += int(stale and shares[symbol] > 0)
            holdings.append({"trade_date": date, "symbol": symbol, "quantity": shares[symbol],
                             "raw_close_observed": close, "valuation_mark": mark, "valuation_is_stale": stale,
                             "market_value": value, "daily_buy_quantity": max(0, shares[symbol] - start_shares[symbol])})
        equity = cash + holding_value
        running_peak = max(running_peak, equity)
        daily_rows.append({"trade_date": date, "nav": equity / initial_cash, "equity": equity,
                           "daily_return": equity / previous_equity - 1, "cash": cash,
                           "holding_value": holding_value, "drawdown": equity / running_peak - 1,
                           "commission": commission_day, "sell_tax": tax_day, "slippage_cost": slippage_day,
                           "total_trade_cost": commission_day + tax_day + slippage_day,
                           "turnover_notional_mid": turnover_notional,
                           "gross_turnover": turnover_notional / pretrade_equity,
                           "pretrade_equity": pretrade_equity, "stale_held_count": stale_held_count,
                           "is_execution_day": date in events})
        assert cash >= -1e-6 and all(q >= 0 and q % lot_size == 0 for q in shares.values())
        previous_equity = equity
    daily = pd.DataFrame(daily_rows)
    holding_table = pd.DataFrame(holdings)
    equity_by_date = daily.set_index("trade_date").equity
    holding_table["realized_close_weight"] = holding_table.market_value / holding_table.trade_date.map(equity_by_date)
    return {"daily": daily, "holdings": holding_table, "orders": pd.DataFrame(orders), "trades": pd.DataFrame(trades),
            "weights": pd.DataFrame(weights), "metrics": metric_summary(daily)}


def manual_example() -> dict:
    weights, returns, assumed_cost = [.5, .5], [.02, -.01], .002
    gross = sum(w * r for w, r in zip(weights, returns))
    net = gross - assumed_cost
    assert math.isclose(gross, .005, abs_tol=1e-12) and math.isclose(net, .003, abs_tol=1e-12)
    return {"weights": weights, "asset_returns": returns, "gross_return": gross,
            "assumed_total_cost_fraction": assumed_cost, "net_return": net,
            "note": "Independent arithmetic example; assumed 20bp total cost is not the execution engine fee schedule"}


def research_split_audit(processed: pd.DataFrame, calendar: pd.DatetimeIndex) -> pd.DataFrame:
    """Recheck lecture 04's mature X-Y rule; these labels never enter the trading engine."""
    frame = processed.copy()
    grouped = frame.groupby("symbol", sort=False)
    frame["audit_label_end"] = grouped["trade_date"].shift(-20)
    frame["audit_label"] = grouped["adj_close"].transform(
        lambda s: (s.shift(-20) / s - 1).where(s.rolling(21, min_periods=1).count().shift(-20).eq(21)))
    frame["audit_xy"] = frame[["mom20_score", "vol20_score", "turn20_score", "audit_label"]].notna().all(axis=1)
    rows = []
    for name, start, stop in [("development", 0, 40), ("validation", 40, 60), ("test", 60, 80)]:
        first, last = str(calendar[start].date()), str(calendar[stop-1].date())
        segment = frame[frame.trade_date.between(first, last)]
        usable = segment.audit_xy & segment.audit_label_end.notna() & segment.audit_label_end.le(last)
        rows.append({"split": name, "start_index": start, "stop_index_exclusive": stop,
                     "lecture04_formal_usable_xy_pairs": int(usable.sum()),
                     "interpretation": "Same 80-date data insufficient for formal three-stage factor evaluation; no OOS claim"})
    return pd.DataFrame(rows)


def validate_run(processed, market, calendar, schedule, scores, targets, results) -> dict:
    module, _ = load_factor_module()
    universe = module.UNIVERSE
    checks = {}
    assert len(processed) == 640 and not processed.duplicated(["symbol", "trade_date"]).any()
    assert processed.adj_close.isna().sum() == 3
    checks["unchanged_complete_factor_grid_and_missing_prices"] = True
    raw_nonmissing = processed[["close_raw", "adj_close"]].dropna()
    assert raw_nonmissing.close_raw.eq(raw_nonmissing.adj_close).all()
    checks["raw_equals_adjusted_only_in_no_corporate_action_simulation"] = True
    assert schedule.execution_date.notna().sum() == 3 and pd.isna(schedule.execution_date.iloc[-1])
    assert schedule.iloc[-1].signal_kind == "terminal_partial_month_audit"
    checks["three_monthly_executions_terminal_snapshot_not_executed"] = True
    for result in results.values():
        daily, holdings, trades = result["daily"], result["holdings"], result["trades"]
        assert daily.cash.ge(-1e-6).all() and holdings.quantity.ge(0).all() and holdings.quantity.mod(LOT_SIZE).eq(0).all()
        assert all(trades.trade_date > trades.signal_date)
        assert daily.loc[daily.trade_date.lt(schedule.execution_date.iloc[0]), "nav"].eq(1).all()
        assert math.isclose(float((1 + daily.daily_return).prod()), float(daily.nav.iloc[-1]), rel_tol=1e-12)
        assert ((daily.equity - daily.cash - daily.holding_value).abs() < 1e-7).all()
        regrouped = holdings.groupby("trade_date").market_value.sum()
        assert (regrouped - daily.set_index("trade_date").holding_value).abs().max() < 1e-7
        if len(result["weights"]):
            opening = result["weights"].groupby("trade_date").first()
            costs = daily.set_index("trade_date").total_trade_cost.reindex(opening.index)
            assert ((opening.pretrade_equity - opening.after_trade_equity - costs).abs() < 1e-7).all()
        trade_turnover = trades.assign(mid_notional=trades.quantity * trades.open_quote).groupby("trade_date").mid_notional.sum()
        expected_turnover = daily.trade_date.map(trade_turnover).fillna(0) / daily.pretrade_equity
        assert (expected_turnover - daily.gross_turnover).abs().max() < 1e-12
        with_initial = pd.Series([1.0] + daily.nav.tolist())
        assert math.isclose(float((with_initial / with_initial.cummax() - 1).min()), result["metrics"]["max_drawdown"], abs_tol=1e-12)
        # One side per stock per daily event plus sale <= holdings available before that date.
        if len(trades):
            assert trades.groupby(["trade_date", "symbol"]).side.nunique().le(1).all()
            start = holdings.sort_values(["symbol", "trade_date"]).groupby("symbol").quantity.shift(1).fillna(0)
            available = holdings.assign(start_quantity=start).set_index(["trade_date", "symbol"]).start_quantity
            for row in trades[trades.side.eq("sell")].to_dict("records"):
                assert row["quantity"] <= available.loc[(row["trade_date"], row["symbol"])]
    for name in ["cash_never_negative", "integer_lots_and_long_only", "signals_execute_at_next_open_only",
                 "cash_warmup_not_backdated", "daily_nav_cash_shares_reconcile", "nav_cumprod_matches_ledger",
                 "opening_equity_loses_costs_exactly_once", "gross_turnover_matches_filled_mid_notional",
                 "drawdown_includes_initial_one", "no_sale_of_same_day_new_purchases"]:
        checks[name] = True
    multi = results[("multi", "base")]
    assert multi["orders"].status.eq("synthetic_open_auction_halt").any()
    assert multi["orders"].status.eq("synthetic_buy_blocked").any()
    assert multi["orders"].status.eq("synthetic_sell_blocked").any()
    checks["actual_orders_exercise_auction_buy_and_sell_blocks"] = True
    assert multi["daily"].stale_held_count.gt(0).any()
    stale_row = multi["holdings"][multi["holdings"].trade_date.eq(str(calendar[30].date())) & multi["holdings"].symbol.eq("SIM001")].iloc[0]
    assert stale_row.quantity > 0 and stale_row.valuation_is_stale and pd.isna(stale_row.raw_close_observed)
    checks["missing_close_valuation_flagged_without_factor_fill"] = True
    zero = results[("multi", "zero")]["daily"]
    assert zero[["commission", "sell_tax", "slippage_cost"]].eq(0).all().all()
    checks["zero_cost_is_full_separate_ledger_rerun"] = True
    constant = pd.DataFrame({"nav": [1., 1., 1.], "daily_return": [0., 0., 0.], "drawdown": [0., 0., 0.]})
    stats = metric_summary(constant)
    assert pd.isna(stats["sharpe"]) and stats["annualized_vol"] == 0 and stats["max_drawdown"] == 0
    first_loss = pd.DataFrame({"nav": [.9, .95], "daily_return": [-.1, .95/.9-1], "drawdown": [-.1, -.05]})
    assert metric_summary(first_loss)["max_drawdown"] == -.1
    checks["constant_returns_and_initial_loss_metric_edges"] = True
    assert math.isclose(manual_example()["net_return"], .003, abs_tol=1e-12)
    checks["independent_two_stock_cost_example"] = True
    # Change only future prices and turnover: past raw factors, scores and targets stay identical.
    raw, _ = module.make_teaching_data()
    cutoff = str(calendar[65].date())
    changed = raw.copy()
    changed.loc[changed.trade_date.ge(cutoff), "adj_close"] *= 1.5
    changed.loc[changed.trade_date.ge(cutoff), "close_raw"] *= 1.5
    changed.loc[changed.trade_date.ge(cutoff), "turnover_rate"] *= 1.8
    changed_factors, _ = module.preprocess_factors(module.compute_factors(changed, calendar, universe))
    changed_factors["multi_score"] = changed_factors[[f"{f}_score" for f in module.FACTORS]].mean(axis=1, skipna=False)
    columns = ["symbol", "trade_date", "mom20", "vol20", "turn20", "mom20_score", "vol20_score", "turn20_score"]
    pd.testing.assert_frame_equal(processed.loc[processed.trade_date.lt(cutoff), columns].reset_index(drop=True),
                                  changed_factors.loc[changed_factors.trade_date.lt(cutoff), columns].reset_index(drop=True))
    changed_market = make_execution_market(changed_factors, calendar, universe)
    pd.testing.assert_series_equal(market.loc[market.trade_date.le(cutoff), "open_quote"].reset_index(drop=True),
                                   changed_market.loc[changed_market.trade_date.le(cutoff), "open_quote"].reset_index(drop=True))
    checks["future_changes_do_not_rewrite_past_factors_or_current_open"] = True
    _, changed_targets = build_signals(changed_factors, schedule, universe)
    pd.testing.assert_frame_equal(targets[targets.signal_date.lt(cutoff)].reset_index(drop=True),
                                  changed_targets[changed_targets.signal_date.lt(cutoff)].reset_index(drop=True))
    changed_result = simulate(changed_market, changed_targets, calendar, universe)
    pd.testing.assert_frame_equal(multi["daily"][multi["daily"].trade_date.lt(cutoff)].reset_index(drop=True),
                                  changed_result["daily"][changed_result["daily"].trade_date.lt(cutoff)].reset_index(drop=True))
    checks["future_changes_preserve_past_targets_and_ledger"] = True
    assert research_split_audit(processed, calendar).lecture04_formal_usable_xy_pairs.eq(0).all()
    checks["fixed_split_matured_xy_counts_remain_zero"] = True
    assert targets[targets.strategy.eq("reference")].groupby("signal_date").target_weight.sum().eq(1).all()
    for strategy in STRATEGIES[:-1]:
        candidate_counts = scores[scores.strategy.eq(strategy)].groupby("signal_date").n_eligible.first()
        assert candidate_counts.equals(scores[scores.strategy.eq("multi")].groupby("signal_date").n_eligible.first())
    checks["common_signal_candidates_and_same_execution_rules"] = True
    return checks


def run(output: Path) -> dict:
    output = output.resolve()
    marker = output / ".quant_babies_lecture05_backtest"
    if output.exists() and (not output.is_dir() or (any(output.iterdir()) and not marker.is_file())):
        raise FileExistsError(f"Refusing to overwrite a non-lab directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    marker.write_text("SIMULATED ledger outputs only.\n", encoding="utf-8")
    processed, market, calendar, provenance = build_inputs()
    module, _ = load_factor_module()
    raw, _ = module.make_teaching_data()
    raw.to_csv(output / "raw_simulated.csv", index=False)
    pd.DataFrame({"trade_date": calendar.strftime("%Y-%m-%d")}).to_csv(output / "calendar_simulated.csv", index=False)
    schedule = make_schedule(calendar)
    scores, targets = build_signals(processed, schedule, module.UNIVERSE)
    processed.to_csv(output / "factor_panel_simulated.csv", index=False)
    market.to_csv(output / "execution_market_simulated.csv", index=False)
    schedule.to_csv(output / "signal_schedule.csv", index=False)
    scores.to_csv(output / "score_rankings.csv", index=False)
    targets.to_csv(output / "frozen_targets.csv", index=False)
    results, metric_rows, nav_frames = {}, [], []
    for strategy in STRATEGIES:
        for scenario in COSTS:
            result = simulate(market, targets, calendar, module.UNIVERSE, strategy, scenario)
            results[(strategy, scenario)] = result
            metric_rows.append({"strategy": strategy, "scenario": scenario, **result["metrics"],
                                "total_commission": float(result["daily"].commission.sum()),
                                "total_sell_tax": float(result["daily"].sell_tax.sum()),
                                "total_slippage_cost": float(result["daily"].slippage_cost.sum()),
                                "total_trade_cost": float(result["daily"].total_trade_cost.sum()),
                                "total_gross_turnover": float(result["daily"].gross_turnover.sum()),
                                "filled_trades": len(result["trades"])})
            for key in ["daily", "holdings", "orders", "trades", "weights"]:
                result[key].to_csv(output / f"{strategy}_{scenario}_{key}.csv", index=False)
            nav_frames.append(result["daily"].assign(strategy=strategy, scenario=scenario))
    metrics = pd.DataFrame(metric_rows)
    metrics.to_csv(output / "performance_metrics.csv", index=False)
    combined = pd.concat(nav_frames, ignore_index=True)
    combined.to_csv(output / "all_nav_series.csv", index=False)
    checks = validate_run(processed, market, calendar, schedule, scores, targets, results)
    second_execution = schedule.execution_date.dropna().iloc[1]
    ranking_snapshot = scores[scores.strategy.eq("multi") & scores.signal_date.eq(schedule.signal_date.iloc[0])]
    weight_snapshot = results[("multi", "base")]["weights"]
    weight_snapshot = weight_snapshot[weight_snapshot.trade_date.eq(second_execution)]
    split_rows = records(research_split_audit(processed, calendar))
    pd.DataFrame(split_rows).to_csv(output / "research_split_notice.csv", index=False)
    config = {"initial_cash": INITIAL_CASH, "lot_size": LOT_SIZE, "top_n": TOP_N,
              "factor_directions": module.DIRECTIONS, "factor_weights": {f: 1/3 for f in module.FACTORS},
              "costs": COSTS, "cost_note": "Fictional decimal rates; not current or historical A-share fees; no minimum commission",
              "execution": "signal after close, next grid opening; sell old shares before cash-limited buys; unfilled expire",
              "opening_quote": "previous close_raw*(1+0.001*sin(0.37*date_index+stock_index)); never current/future close",
              "valuation": "observed raw close; last observed close only for flagged valuation on missing-close dates",
              "turnover": "sum(abs(filled_quantity)*opening_mid_quote)/pretrade_open_equity, gross L1; no division by two",
              "cash_rate": 0.0, "daily_risk_free": 0.0, "annualization_days": 252}
    summary = {"data_kind": DATA_KIND, "start_date": str(calendar[0].date()), "end_date": str(calendar[-1].date()),
               "calendar_note": "80 pandas business dates, NOT an A-share exchange calendar",
               "config": config, "strategies": STRATEGIES, "schedule": records(schedule),
               "ranking_snapshot": records(ranking_snapshot), "weight_snapshot": records(weight_snapshot),
               "nav_series": records(combined), "metrics": records(metrics),
               "cost_sensitivity": records(metrics[metrics.strategy.eq("multi")]),
               "manual": manual_example(), "splits": split_rows, "checks": checks}
    (output / "chart_data.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    blocked = results[("multi", "base")]["orders"].status.value_counts().to_dict()
    report = {"data_kind": DATA_KIND, **provenance, "calendar_dates": len(calendar), "symbols": len(module.UNIVERSE),
              "executable_signals": int(schedule.execution_date.notna().sum()),
              "terminal_snapshot_is_partial_month": True, "multi_base_order_status_counts": blocked,
              "multi_base_metrics": next(row for row in metric_rows if row["strategy"] == "multi" and row["scenario"] == "base"),
              "config": config, "checks": checks, "pandas_version": pd.__version__,
              "limitations": ["Small synthetic data and three executions; no real or OOS validity claim",
                              "No order book, intraday paths, real limit queues, delisting, dividends or corporate actions",
                              "Deterministic buy priority, no minimum commission, expired unfilled orders, flagged stale valuation",
                              "Top3 and 100-share lots are teaching conventions; benchmark is simulated equalweight portfolio"]}
    (output / "quality_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/processed/lecture05-simulation"))
    args = parser.parse_args()
    try:
        report = run(args.output)
    except (OSError, ValueError, AssertionError) as exc:
        print(f"Backtest lab failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({k: report[k] for k in ["data_kind", "grid_rows", "executable_signals", "multi_base_order_status_counts", "multi_base_metrics", "checks"]}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
