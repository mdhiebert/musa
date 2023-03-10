from company import Company

from typing import List, Union

class Ecosystem:

    def __init__(self, companies: List[Company]):
        self.companies = companies

    def add_company(self, new_company: Company) -> None:
        self.companies.append(new_company)

    def get_companies_by_industry_id(self, industry_id: str) -> List[Company]:
        return [
            company for company in self.companies if industry_id in [i.id for i in company.industries]
        ]

    def get_company_by_ticker(self, ticker: str) -> Union[Company, None]:
        for company in self.companies:
            if company.ticker == ticker: return company
        return None