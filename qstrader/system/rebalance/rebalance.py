from __future__ import annotations

from abc import ABCMeta, abstractmethod

import pandas as pd


class Rebalance(object):
    """
    Interface to a generic list of system logic and
    trade order rebalance timestamps.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.rebalances: list[pd.Timestamp] | None = None

    @abstractmethod
    def output_rebalances(self):
        raise NotImplementedError("Should implement output_rebalances()")
