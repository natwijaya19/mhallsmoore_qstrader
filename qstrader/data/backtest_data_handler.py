import numpy as np
import pandas as pd

from qstrader.asset.universe.universe import Universe
from qstrader.data.daily_bar_csv import CSVDailyBarDataSource
from qstrader.data.data_handler import DataHandler
from qstrader.data.data_source import BarDataSource


class BacktestDataHandler(DataHandler):
    """
    This class provides an interface for obtaining historical
    pricing data and asset information from a set of DataSources.
    """

    def __init__(
        self, universe: Universe, data_sources: list[BarDataSource] = None
    ):
        self.universe: Universe = universe
        self.data_sources: list[BarDataSource] = data_sources

    def get_asset_latest_bid_price(self, dt: pd.Timestamp, asset_symbol: str) -> float:
        """
        Get the latest bid price for a given asset.
        """
        # TODO: Check for asset in Universe
        bid: float = np.NaN
        for ds in self.data_sources:
            try:
                bid = ds.get_bid(dt, asset_symbol)
                if not np.isnan(bid):
                    return bid
            except Exception:
                bid = np.NaN
        return bid

    def get_asset_latest_ask_price(self, dt: pd.Timestamp, asset_symbol: str) -> float:
        """
        Get the latest ask price for a given asset.
        """
        # TODO: Check for asset in Universe
        ask: float = np.NaN
        for ds in self.data_sources:
            try:
                ask = ds.get_ask(dt, asset_symbol)
                if not np.isnan(ask):
                    return ask
            except Exception:
                ask = np.NaN
        return ask

    def get_asset_latest_bid_ask_price(
        self, dt: pd.Timestamp, asset_symbol: str
    ) -> tuple[float, float]:
        """
        Get the latest bid/ask price for a given asset.
        """
        # TODO: For the moment this is sufficient for OHLCV
        # data, which only usually provides mid prices
        # This will need to be revisited when handling intraday
        # bid/ask time series.
        # It has been added as an optimisation mechanism for
        # interday backtests.
        bid: float = self.get_asset_latest_bid_price(dt, asset_symbol)
        ask: float = self.get_asset_latest_ask_price(dt, asset_symbol)
        return bid, ask

    def get_asset_latest_mid_price(self, dt: pd.Timestamp, asset_symbol: str):
        """
        Get the latest mid price for a given asset.
        """
        bid_ask: tuple[float, float] = self.get_asset_latest_bid_ask_price(
            dt, asset_symbol
        )
        try:
            mid: float = (bid_ask[0] + bid_ask[1]) / 2.0
        except Exception:
            # TODO: Log this
            raise ValueError(
                f"Could not calculate mid price for {asset_symbol} at {dt}"
            )
            # mid = np.NaN
        return mid

    def get_assets_historical_range_close_price(
        self,
        start_dt: pd.Timestamp,
        end_dt: pd.Timestamp,
        asset_symbols: list[str],
        adjusted=False,
    ):
        """
        Get the historical range of close prices for a given
        set of assets.
        """
        prices_df: pd.DataFrame | None = None
        for ds in self.data_sources:
            try:
                prices_df = ds.get_assets_historical_closes(
                    start_dt,
                    end_dt,
                    asset_symbols,  # adjusted=adjusted
                )
                if prices_df is not None:
                    return prices_df
            except Exception:
                raise
        return prices_df
