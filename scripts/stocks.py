from musa.market.stock import Stock
from datetime import date


s = Stock('TEST', 'NASDAQ',
            (date(2023, 2, 23),),
            ((0,1,2,3,4,5),)
        )