import pathlib
from pathlib import Path

import pandas as pd
import pytz

from qstrader.alpha_model.fixed_signals import FixedSignalsAlphaModel
from qstrader.asset.equity import Equity
from qstrader.asset.universe.static import StaticUniverse
from qstrader.asset.universe.universe import Universe
from qstrader.data.backtest_data_handler import BacktestDataHandler
from qstrader.data.daily_bar_csv import CSVDailyBarDataSource
from qstrader.statistics.tearsheet import TearsheetStatistics
from qstrader.trading.backtest import BacktestTradingSession

if __name__ == "__main__":
    start_dt: pd.Timestamp = pd.Timestamp("2003-09-30 14:30:00", tz=pytz.UTC)
    end_dt: pd.Timestamp = pd.Timestamp("2019-12-31 23:59:00", tz=pytz.UTC)

    # Construct the symbols and assets necessary for the backtest
    strategy_symbols: list[str] = ["SPY", "AGG"]
    strategy_assets: list[str] = ["EQ:%s" % symbol for symbol in strategy_symbols]
    strategy_universe: Universe = StaticUniverse(strategy_assets)

    # To avoid loading all CSV files in the directory, set the
    csv_dir: Path = pathlib.Path("..", "data")
    data_source: CSVDailyBarDataSource = CSVDailyBarDataSource(
        csv_dir=str(csv_dir), asset_type=Equity, csv_symbols=strategy_symbols
    )
    data_handler: BacktestDataHandler = BacktestDataHandler(
        strategy_universe, data_sources=[data_source]
    )

    # Construct an Alpha Model that simply provides
    # static allocations to a universe of assets
    # In this case 60% SPY ETF, 40% AGG ETF,
    # rebalanced at the end of each month
    strategy_alpha_model: FixedSignalsAlphaModel = FixedSignalsAlphaModel(
        {"EQ:SPY": 0.6, "EQ:AGG": 0.4}
    )

    strategy_backtest: BacktestTradingSession = BacktestTradingSession(
        start_dt=start_dt,
        end_dt=end_dt,
        universe=strategy_universe,
        alpha_model=strategy_alpha_model,
        rebalance="end_of_month",
        long_only=True,
        cash_buffer_percentage=0.01,
        data_handler=data_handler,
    )

    strategy_backtest.run()

    # Construct benchmark assets (buy & hold SPY)
    benchmark_assets = ["EQ:SPY"]
    benchmark_universe = StaticUniverse(benchmark_assets)

    # Construct a benchmark Alpha Model that provides
    # 100% static allocation to the SPY ETF, with no rebalance
    benchmark_alpha_model = FixedSignalsAlphaModel({"EQ:SPY": 1.0})
    benchmark_backtest = BacktestTradingSession(
        start_dt,
        end_dt,
        benchmark_universe,
        benchmark_alpha_model,
        rebalance="buy_and_hold",
        long_only=True,
        cash_buffer_percentage=0.01,
        data_handler=data_handler,
    )
    benchmark_backtest.run()

    # Performance Output
    tearsheet = TearsheetStatistics(
        strategy_equity=strategy_backtest.get_equity_curve(),
        benchmark_equity=benchmark_backtest.get_equity_curve(),
        title="60/40 US Equities/Bonds",
    )
    tearsheet.plot_results()
