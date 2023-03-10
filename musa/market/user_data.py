from typing import List
from transaction import Transaction
from musa.market.stock import StockDatum

class UserData:
    def __init__(self, liquidity: float, transactions: List[Transaction] = None):
        self.liquidity = liquidity
        self.transactions = transactions if transactions is not None else []

    @property
    def open_transactions(self) -> List[Transaction]:
        return [transaction for transaction in self.transactions if not transaction.is_closed]
    
    def can_buy(self, stock_data: StockDatum, volume: float):
        '''
            Returns True if the user has enough liquidity to afford this volume of stock, else False.
        '''
        return (stock_data.average * volume) <= self.liquidity
    
    def buy(self, stock_data: StockDatum, volume: float):
        '''
            Purchase `volume` worth of `stock_data.ticker` stock with information `stock_data`. This will subtract `volume * stock_data.average` amount from self.liquidity and insert a new transaction representing this purchase into self.transactions.
        '''

        assert self.can_buy(stock_data, volume), 'User cannot afford this volume of this stock.'

        expenditure = volume * stock_data.average

        self.liquidity -= expenditure

        self.transactions.append(Transaction(stock_data, volume))

    def does_own(self, ticker: str) -> bool:
        '''
            Returns True if this user owns the given ticker at this time, else False
        '''
        for transaction in self.transactions:
            if not transaction.is_closed and transaction.enter.ticker == ticker: return True
        return False
    
    def sell(self, stock_data: StockDatum):
        '''
            Sells ALL of this user's holdings of the given stock, closing out each Transaction where this stock was bought and not yet sold.
        '''

        for transaction in self.open_transactions:
            if transaction.enter.ticker == stock_data.ticker:

                # set the exit data of the transaction
                transaction.sell(stock_data)

                # add the ROI to the liquidity
                self.liquidity += transaction.roi
    
    def asset_worth(self, closing_data: List[StockDatum]):
        '''
            Returns the total value of this users assets (liquidity + sum(projected_transaction_rois)).

            Parameters
            ----------
            closing_data :: List[StockData] : a list of length `num_of_open_transactions` where the nth item of `closing_data` aligns with the nth open transaction sequentially in `self.transactions`
        '''

        running_value = self.liquidity

        for transaction in self.open_transactions:
            running_value += transaction.projected_return_on_investment(closing_data.pop(0))
