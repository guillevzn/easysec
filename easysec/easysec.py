import requests
import json
import pandas as pd

class easysec():
    BASE_URL = 'https://data.sec.gov/'

    def __init__(self, headers: dict, cik = None):
        self.headers = headers
        self.cik = None

    def companytickers(self):
        response = requests.get(
        'https://www.sec.gov/files/company_tickers.json',
        headers = self.headers)
        data = json.loads(response.text)
        df = pd.DataFrame.from_dict(data, orient='index')
        df['cik_str'] = df['cik_str'].astype(str).str.zfill(10)
        return df

    def set_company(self, cik: str):
        self.cik = cik.zfill(10)
    
    def companydata(self):
        if self.cik == None:
            raise ValueError('You must specify a CIK code.')
        response = requests.get(
        self.BASE_URL + f'submissions/CIK{self.cik}.json',
        headers = self.headers)
        data = json.loads(response.text)

        del data['filings']
        df = pd.json_normalize(data).T
        
        return df
    
    def submissions(self):
        if self.cik == None:
            raise ValueError('You must specify a CIK code.')
        response = requests.get(
        self.BASE_URL + f'submissions/CIK{self.cik}.json',
        headers = self.headers)
        data = json.loads(response.text)

        df = pd.DataFrame.from_dict(data['filings']['recent'])

        return df
    
    def companyconcept(self):
        if self.cik == None:
            raise ValueError('You must specify a CIK code.')
        response = requests.get(
        self.BASE_URL + f'api/xbrl/companyconcept/CIK{self.cik}.json',
        headers = self.headers)
        data = json.loads(response.text)
        return data

    def companyfacts(self):
        if self.cik == None:
            raise ValueError('You must specify a CIK code.')
        response = requests.get(
        self.BASE_URL + f'api/xbrl/companyfacts/CIK{self.cik}.json',
        headers = self.headers)
        data = json.loads(response.text)

        us_gaaps = [*data['facts']['us-gaap']]

        dfs_us_gaaps = list()
        for us_gaap in us_gaaps:
            cik_value = data['cik']
            entityName_value = data['entityName']
            label_key = data['facts']['us-gaap'][us_gaap]['label']
            description_key = data['facts']['us-gaap'][us_gaap]['description']
            unit_key = next(iter(data['facts']['us-gaap'][us_gaap]['units'].keys()))

            temp_df = pd.json_normalize(data['facts']['us-gaap'][us_gaap]['units'][unit_key])

            temp_df.insert(0, 'unit', unit_key)
            temp_df.insert(0, 'description', description_key)
            temp_df.insert(0, 'label', label_key)
            temp_df.insert(0, 'us-gaap', us_gaap)
            temp_df.insert(0, 'entityName', entityName_value)
            temp_df.insert(0, 'cik', cik_value)
            dfs_us_gaaps.append(temp_df)
        
        df = pd.concat(dfs_us_gaaps)
        df['cik'] = df['cik'].astype(str).str.zfill(10)
        df.reset_index(inplace=True)
        return df

    def frames(self, tag: str, uom: str, ccp: str):
        if self.cik == None:
            raise ValueError('You must specify a CIK code.')
        response = requests.get(
        self.BASE_URL + f'api/xbrl/frames/us-gaap/{tag}/{uom}/{ccp}.json',
        headers = self.headers)
        data = json.loads(response.text)
        return data