# %%
import requests

class easysec():
    BASE_URL = "https://data.sec.gov/api"

    def __init__(self):
        self.session = requests.Session()

    def get_filings(self, company_cik, filing_type):
        url = f"{self.BASE_URL}/companies/{company_cik}/filings"
        params = {
            "type": filing_type,
            "date": "",
            "count": 100,
            "output": "json"
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()

        # Process the JSON response here
        data = response.json()
        filings_data = data["filings"]

        # Process and return the filings data as per your requirement
        processed_data = []
        for filing in filings_data:
            filing_data = {
                "access_number": filing["accessionNumber"],
                "filing_date": filing["filingDate"],
                "form_type": filing["formType"],
                "description": filing["description"],
                "link": filing["linkToHtml"]
            }
            processed_data.append(filing_data)

        return processed_data
    
data_importer = easysec()
filings = data_importer.get_filings("0000320193", "10-K")

for filing in filings:
    print(filing)
# %%
