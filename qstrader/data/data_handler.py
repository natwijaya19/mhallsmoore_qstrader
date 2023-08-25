import abc

import pandas as pd


class DataHandler(abc.ABC):
    """
    This class provides an interface for obtaining historical
    pricing data and asset information from a set of DataSources.
    """

    # def __init__( self, universe: Universe, data_sources: list[
    # CSVDailyBarDataSource] = None ): raise NotImplementedError("Should
    # implement DataHandler.__init__()")

    @abc.abstractmethod
    def get_asset_latest_bid_price(self, dt: pd.Timestamp, asset_symbol: str) -> float:
        """
        Get the latest bid price for a given asset.
        """
        # TODO: Check for asset in Universe
        raise NotImplementedError(
            "Should implement DataHandler.get_asset_latest_bid_price()"
        )

    @abc.abstractmethod
    def get_asset_latest_ask_price(self, dt: pd.Timestamp, asset_symbol: str) -> float:
        """
        Get the latest ask price for a given asset.
        """
        # TODO: Check for asset in Universe
        raise NotImplementedError(
            "Should implement DataHandler.get_asset_latest_ask_price()"
        )

    @abc.abstractmethod
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
        raise NotImplementedError(
            "Should implement DataHandler.get_asset_latest_bid_ask_price()"
        )

    @abc.abstractmethod
    def get_asset_latest_mid_price(self, dt: pd.Timestamp, asset_symbol: str):
        """
        Get the latest mid price for a given asset.
        """
        raise NotImplementedError(
            "Should implement DataHandler.get_asset_latest_mid_price()"
        )

    @abc.abstractmethod
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
        raise NotImplementedError(
            "Should implement DataHandler.get_assets_historical_range_close_price()"
        )
