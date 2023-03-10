from typing import List, Tuple

import os

class AbstractHistoricalDataGatherer:

    def __init__(self, market_name: str):
        self.market_name = market_name

    def gather_data_for_ticker(self, ticker: str) -> List[Tuple[str, str, str, float, float, float, float, float, int]]:
        '''
            Parameters
            ----------
            ticker :: str : the ticker for a particular security in this market

            Returns
            -------
            A List of Tuple representing (date, market_name, ticker_name, open, high, low, close, adjusted_close, volume)
        '''
        raise NotImplementedError

    def gather_data_for_tickers(self, tickers: List[str]) -> List[List[Tuple[str, str, str, float, float, float, float, float, int]]]:
        return [self.gather_data_for_ticker(ticker) for ticker in tickers]

    def write_data_for_tickers(self, tickers: List[str], dirpath: str) -> None:
        '''
            Writes the data gathered for tickers into a series of CSVs under dirpath, creating the directory if necessary
        '''

        # try to create the directory
        try:
            os.mkdir(dirpath)
        except FileExistsError as fee:
            pass # it already exists

        for ticker in tickers:
            ticker_data = self.gather_data_for_ticker(ticker)

            with open(f'{dirpath}/{ticker}.csv', 'w+') as f:
                f.write(
                    [ticker_tuple.join(',') for ticker_tuple in ticker_data].join('\n')
                )

class NASDAQHDG(AbstractHistoricalDataGatherer):
    def __init__(self):
        super().__init__('NASDAQ')

    def gather_data_for_ticker(self, ticker: str) -> List[Tuple[str, str, str, float, float, float, float, float, int]]:
        
        # TODO
        pass