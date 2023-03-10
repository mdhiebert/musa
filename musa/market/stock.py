from typing import List, Tuple, Generator, Iterable
from datetime import timedelta, datetime

import datetime

class StockDatum:
    @staticmethod
    def from_str(s: str):
        '''
            Converts data of the form `(date, market, ticker, open, high, low, close, adjusted_close, volume) into a StockData object
        '''
        date, market, ticker, open, high, low, close, adjusted_close, volume = s.split(',')

        date = datetime.strptime(date, '%Y-%m-%d')
        open = float(open)
        high = float(high)
        low = float(low)
        close = float(close)
        adjusted_close = float(adjusted_close)
        volume = int(volume)

        return StockDatum(date, market, ticker, open, high, low, close, adjusted_close, volume)

    def __init__(self, date: datetime.date, market_name: str, ticker_name: str, open: float, high: float, low: float, close: float, adj_close: float, volume: int):
        self.date = date
        self.market_name = self.market = market_name
        self.ticker_name = self.ticker = ticker_name

        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.adjusted_close = self.adj_close = adj_close
        self.volume = volume

    @property
    def average(self):
        return (self.high - self.low) / 2

    def __iter__(self):
        yield self.date
        yield self.market_name
        yield self.ticker_name
        yield self.open
        yield self.high
        yield self.low
        yield self.close
        yield self.adjusted_close
        yield self.volume

    def __str__(self):
        return self.date.strftime('%Y-%m-%d,') + ','.join(list(self[1:]))
    
class StockValue(float):
    pass

class Stock:
    '''
        A `Stock` is an abstract representation of a specific market-traded stock which keeps track of 
        its historical and current values as well as useful analysis, calculations, or alternate representations
        of that data.
    '''
    def __init__(self,
        ticker: str,
        market_name: str
    ):
        self.ticker_name = self.ticker = ticker
        self.market_name = self.market = market_name


        # I think it is best if all stock information ever is
        # not stored in memory, but `Stock` instead acts as
        # an interface to retrieve that information from a database
        # self.data: List[StockDatum] = list(stock_data)

        self.last_updated = None
        self.current_value = None

    @property
    def has_value(self):
        return self.current_value is not None

    #================================================
    #                DATA FUNCTIONS
    #================================================

    def get_data_for_date(self, date: datetime.date):
        raise NotImplementedError

    def generate_stock_data(self) -> Generator[StockDatum]:
        '''
            Yields data for this stock in the given time range as StockData objects`
        '''

        for i,value in enumerate(self.values):
            stock_open, stock_high, stock_low, stock_close, stock_adj_close, stock_volume = value
            date = self.start_date + timedelta(days = i)

            yield StockDatum(
                date = date,
                market_name = self.market,
                ticker_name = self.ticker,
                open = stock_open,
                high = stock_high,
                low = stock_low,
                close = stock_close,
                adj_close = stock_adj_close,
                volume = stock_volume
            )
