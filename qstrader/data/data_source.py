import abc

import pandas as pd


class BarDataSource(abc.ABC):
    """
    An abstract base class for providing OHLCV bar data
    to a Strategy.
    """

    @abc.abstractmethod
    def get_bid(self, dt: pd.Timestamp, asset: str) -> float:
        """
        Obtain the bid price of an asset at the provided timestamp.

        Parameters
        ----------
        dt : `pd.Timestamp`
            When to obtain the bid price for.
        asset : `str`
            The asset symbol to obtain the bid price for.

        Returns
        -------
        `float`
            The bid price.
        """
        raise NotImplementedError("Should implement get_bid()!")
    @abc.abstractmethod
    def get_ask(self, dt: pd.Timestamp, asset: str) -> float:
        """
        Obtain the ask price of an asset at the provided timestamp.

        Parameters
        ----------
        dt : `pd.Timestamp`
            When to obtain the ask price for.
        asset : `str`
            The asset symbol to obtain the ask price for.

        Returns
        -------
        `float`
            The ask price.
        """
        raise NotImplementedError("Should implement get_ask()!")

    @abc.abstractmethod
    def get_assets_historical_closes(
        self,
        start_dt: pd.Timestamp,
        end_dt: pd.Timestamp,
        assets: list[str],
    ) -> pd.DataFrame:
        """
        Obtain a multi-asset historical range of closing prices as a DataFrame,
        indexed by timestamp with asset symbols as columns.

        Parameters
        ----------
        start_dt : `pd.Timestamp`
            The starting datetime of the range to obtain.
        end_dt : `pd.Timestamp`
            The ending datetime of the range to obtain.
        assets : `list[str]`
            The list of asset symbols to obtain closing prices for.

        Returns
        -------
        `pd.DataFrame`
            The multi-asset closing prices DataFrame.
        """
        raise NotImplementedError(
            "Should implement get_assets_historical_closes()!"
        )
