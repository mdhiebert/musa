import datetime

from util.holidays import US_MARKET_HOLIDAYS

MON, TUE, WED, THU, FRI, SAT, SUN = list(range(7))
WEEKEND = (SAT, SUN)

def is_trading_day(date: datetime.date):
    return date.weekday not in WEEKEND and date not in US_MARKET_HOLIDAYS

def get_next_trading_day(date: datetime.date, market = 'US'):
    # TODO make it market-specific

    next_day = date + datetime.timedelta(days = 1)

    while (not is_trading_day(next_day)):
        next_day = next_day + datetime.timedelta(days = 1)

    return next_day

def get_previous_trading_day(date: datetime.date, market = 'US'):
    # TODO make it market-specific

    prev_day = date - datetime.timedelta(days = 1)

    while (not is_trading_day(prev_day)):
        prev_day = prev_day - datetime.timedelta(days = 1)

    return prev_day
