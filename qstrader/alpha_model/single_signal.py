from __future__ import annotations

from typing import List

import pandas as pd

from qstrader.alpha_model.alpha_model import AlphaModel
from qstrader.asset.universe.universe import Universe
from qstrader.data.backtest_data_handler import BacktestDataHandler


class SingleSignalAlphaModel(AlphaModel):
    """
    A simple AlphaModel that provides a single scalar forecast
    value for each Asset in the Universe.

    Parameters
    ----------
    universe : `Universe`
        The Assets to make signal forecasts for.
    signal : `float`, optional
        The single fixed floating point scalar value for the signals.
    data_handler : `DataHandler`, optional
        An optional DataHandler used to preserve interface across AlphaModels.
    """

    def __init__(
            self,
            universe: Universe,
            signal: dict[str, float] | float = 1.0,
            data_handler: BacktestDataHandler = None
    ):
        self.universe: Universe = universe
        self.signal: dict[str, float] | float = signal
        self.data_handler: BacktestDataHandler = data_handler

    def __call__(self, dt: pd.Timestamp) -> dict[str, float] | float:
        """
        Produce the dictionary of single fixed scalar signals for
        each of the Asset instances within the Universe.

        Parameters
        ----------
        dt : `pd.Timestamp`
            The time 'now' used to obtain appropriate data and universe
            for the the signals.

        Returns
        -------
        `dict{str: float}`
            The Asset symbol keyed scalar-valued signals.
        """
        assets: list[str] = self.universe.get_assets(dt)
        return {asset: self.signal for asset in assets}
