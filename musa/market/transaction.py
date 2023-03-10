from musa.market.stock import StockDatum

class Transaction:

    def __init__(self, enter_data: StockDatum, volume: float, exit_data: StockDatum = None):
        self.enter_data = self.enter = enter_data
        self.volume = volume
        self.exit_data = self.exit = exit_data


    @property
    def is_closed(self):
        return self.exit is not None
    
    @property
    def return_on_investment(self):
        if self.is_closed:
            return (self.exit_data.average - self.enter_data.average) * self.volume
        else:
            return 0
        
    def sell(self, stock_data: StockDatum):
        self.exit_data = self.exit = stock_data
        
    @property
    def roi(self):
        return self.return_on_investment
    
    def projected_return_on_investment(self, projected_exit_data: StockDatum):
        return Transaction(self.enter, projected_exit_data).roi