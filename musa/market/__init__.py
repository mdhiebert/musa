import datetime
from datetime import timedelta

from musa.market.stock import StockDatum
from musa.market.user_data import UserData

import util.day

from typing import Dict, List

class Market:

    def __init__(self, market_name: str, start_date: datetime.date, tickers: List[str]):
        
        self.market_name = self.market = self.name = market_name
        self.start_date = self.start = start_date

        self.current_date = self.start_date

        self.tickers = tickers

        # to engage with the market, one must self.set_user()
        self.user = None

    #================================================
    #                USER FUNCTIONS
    #================================================

    def set_user(self, user: UserData):
        self.user = user

    def set_new_user_with_liquidity(self, starting_liquidity: float):
        self.set_user(UserData(starting_liquidity))

    #================================================
    #                TIME FUNCTIONS
    #================================================

    def advance_by(self, days: int):
        '''
            Advances the market forward by `days` number of days.

            Parameters
            ----------
            days :: int : a non-negative integer
        '''

        for _ in range(days):
            self.current_date = util.day.get_next_trading_day(self.current_date)
    
    def advance(self):
        '''
            Advances the market by a single day.
        '''
        self.advance_by(days = 1)

    def set_date(self, new_date: datetime.date):
        '''
            Sets the current date to `new_date`
        '''
        self.current_date = new_date

    #================================================
    #                DATA FUNCTIONS
    #================================================

    def get_data_for_ticker_for_date(self, ticker: str, date: datetime.date) -> StockDatum:
        raise NotImplementedError

    def get_data_for_ticker_for_today(self, ticker: str) -> StockDatum:
        return self.get_data_for_ticker_for_date(ticker, self.current_date)

    def get_data_for_all_tickers_for_date(self, date: datetime.date) -> Dict[StockDatum]:
        return {
            ticker: self.get_data_for_ticker_for_date(ticker, date) for ticker in self.tickers
        }
    
    #------------------------------------------------
    #             SLIDING WINDOW FUNCTIONS
    #------------------------------------------------
    
    def get_data_for_ticker_for_date_range(self, ticker: str, start_date: datetime.date, end_date: datetime.date) -> List[StockDatum]:
        '''
            Returns a list of StockData for the given ticker between `start_date` and `end_date` (inclusive).
        '''

        # we use this trick to select the first trading day greater than or equal to our given start date
        running_date = start_date - timedelta(days = 1)
        running_date = util.day.get_next_trading_day(running_date)

        data_to_return = [self.get_data_for_ticker_for_date(ticker, running_date)]
        running_date = util.day.get_next_trading_day(running_date)

        while running_date < end_date:
            data_to_return.append(self.get)
            running_date = util.day.get_next_trading_day(running_date)

        return data_to_return
    
    def get_data_for_ticker_for_dates(self, ticker: str, dates: List[datetime.date]) -> List[StockDatum]:
        '''
            Returns a list of StockData for the given ticker where the nth entry of the returned list corresponds to the StockData for the nth entry of `dates`.
        '''

        return [
            self.get_data_for_ticker_for_date(ticker, date) for date in dates
        ]
    
    def get_previous_n_days_for_ticker(self, ticker: str, n_days: int) -> List[StockDatum]:
        '''
            Returns a list of StockData for the given ticker which includes the current day and the previous `(n_days - 1)` days worth of trading data. The data will be ordered in the list chronologically, with the current date's trading data at the last index.
        '''

        if n_days < 1: return []

        data_to_return = [self.get_data_for_ticker_for_date(ticker, self.current_date)]

        while len(data_to_return) < n_days:
            data_to_return.insert(
                0, self.get_data_for_ticker_for_date(ticker, util.day.get_previous_trading_day(data_to_return[0].date))
            )

        return data_to_return
    

    # 5D
    def get_previous_five_days_for_ticker(self, ticker: str) -> List[StockDatum]:
        return self.get_previous_n_days_for_ticker(ticker, n_days = 5)
    
    # 10D
    def get_previous_ten_days_for_ticker(self, ticker: str) -> List[StockDatum]:
        return self.get_previous_n_days_for_ticker(ticker, n_days = 10)
    
    # YTD
    def get_year_to_date_for_ticker(self, ticker: str) -> List[StockDatum]:
        return self.get_data_for_ticker_for_date_range(ticker, start_date = datetime.date(self.current_date.year, 1, 1), end_date = self.current_date)
    
    # 1Y
    def get_previous_year_for_ticker(self, ticker: str) -> List[StockDatum]:
        return self.get_data_for_ticker_for_date_range(
            ticker, 
            start_date = datetime.date(self.current_date.year - 1, self.current_date.month, self.current_date.day), 
            end_date   = self.current_date
        )
    
    # 5Y
    def get_previous_five_years_for_ticker(self, ticker: str) -> List[StockDatum]:
        return self.get_data_for_ticker_for_date_range(
            ticker, 
            start_date = datetime.date(self.current_date.year - 5, self.current_date.month, self.current_date.day), 
            end_date   = self.current_date
        )


