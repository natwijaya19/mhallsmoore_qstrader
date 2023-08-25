import abc
from abc import ABCMeta, abstractmethod


class TradingSession(abc.ABC):
    """
    Interface to a live or backtested trading session.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        raise NotImplementedError("Should implement run()")
