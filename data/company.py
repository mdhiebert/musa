from typing import Set

from industry import Industry

class Company:

    def __init__(self,
        ticker: str,
        company_name: str,
        industries: Set[Industry]
    ):
        self.ticker = ticker
        self.name = self.company_name = company_name
        self.industries = industries