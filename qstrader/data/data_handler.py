from abc import ABCMeta, abstractmethod


class DataHandler(object, metaclass=ABCMeta):
    @abstractmethod
    def get_asset_latest_bid_price(self, dt, asset_symbol):
        """ """
        pass

    @abstractmethod
    def get_asset_latest_ask_price(self, dt, asset_symbol):
        """ """
        pass

    @abstractmethod
    def get_asset_latest_bid_ask_price(self, dt, asset_symbol):
        """ """
        pass

    @abstractmethod
    def get_asset_latest_mid_price(self, dt, asset_symbol):
        """ """
        pass

    @abstractmethod
    def get_assets_historical_range_close_price(self, start_dt, end_dt,
                                                asset_symbols, adjusted):
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
        pass
