from typing import Tuple

import numpy as np
import pandas as pd

from qstrader.asset.universe.universe import Universe
from qstrader.data.daily_bar_csv import CSVDailyBarDataSource


class BacktestDataHandler(object):
    """ """

    def __init__(
        self, universe: Universe, data_sources: list[CSVDailyBarDataSource] = None
    ):
        self.universe = universe
        self.data_sources = data_sources

    def get_asset_latest_bid_price(self, dt: pd.Timestamp, asset_symbol: str) -> float:
        """ """
        # TODO: Check for asset in Universe
        bid: float = np.NaN
        ds: CSVDailyBarDataSource
        for ds in self.data_sources:
            try:
                bid = ds.get_bid(dt, asset_symbol)
                if not np.isnan(bid):
                    return bid
            except Exception:
                bid = np.NaN
        return bid

    def get_asset_latest_ask_price(self, dt, asset_symbol):
        """ """
        # TODO: Check for asset in Universe
        ask = np.NaN
        ds: CSVDailyBarDataSource
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
    ) -> Tuple[float, float]:
        """ """
        # TODO: For the moment this is sufficient for OHLCV
        # data, which only usually provides mid prices
        # This will need to be revisited when handling intraday
        # bid/ask time series.
        # It has been added as an optimisation mechanism for
        # interday backtests.
        bid: float = self.get_asset_latest_bid_price(dt, asset_symbol)
        return (bid, bid)

    def get_asset_latest_mid_price(self, dt: pd.Timestamp, asset_symbol: str) -> float:
        """ """
        bid_ask: tuple[float, float] = self.get_asset_latest_bid_ask_price(
            dt, asset_symbol
        )
        try:
            mid: float = (bid_ask[0] + bid_ask[1]) / 2.0
        except Exception:
            # TODO: Log this
            mid = np.NaN
        return mid

    def get_assets_historical_range_close_price(
        self,
        start_dt: pd.Timestamp,
        end_dt: pd.Timestamp,
        asset_symbols: list[str],
        adjusted=False,
    ) -> pd.DataFrame:
        """
        Get the historical range of close prices for a list of
        assets between a start and end date.

        Parameterss
        ----------
        start_dt : `pd.Timestamp`
            The starting timestamp of the historical range.
        end_dt : `pd.Timestamp`
            The ending timestamp of the historical range.
        asset_symbols : `list[str]`
            The list of asset symbols to retrieve the historical
            close prices for.
        adjusted : `boolean`, optional
            Whether to retrieve the adjusted close prices.

        Returns
        -------
        `pd.DataFrame`
            The historical close prices for the assets.

        """
        prices_df: pd.DataFrame = pd.DataFrame()
        for ds in self.data_sources:
            try:
                prices_df = ds.get_assets_historical_closes(
                    start_dt,
                    end_dt,
                    asset_symbols,
                    # adjusted=adjusted
                )
                if prices_df is not None:
                    return prices_df
            except Exception:
                raise
        return prices_df
