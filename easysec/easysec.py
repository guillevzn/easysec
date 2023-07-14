import requests
import json
import pandas as pd

class easysec():
    BASE_URL = 'https://data.sec.gov/'

    def __init__(self, headers: dict, cik: str = None):
        self.headers = headers
        if cik:
            self.cik = cik.zfill(10)

    def companytickers(self):
        response = requests.get(
        'https://www.sec.gov/files/company_tickers.json',
        headers = self.headers)
        data = json.loads(response.text)
        df = pd.DataFrame.from_dict(data, orient='index')
        df['cik_str'] = df['cik_str'].astype(str).str.zfill(10)
        return df
    
    def submissions(self, cik: str):
        response = requests.get(
        self.BASE_URL + f'submissions/CIK{cik}.json',
        headers = self.headers)
        data = json.loads(response.text)
        return data
    
    def forms(self, cik: str):

        '''
        Esta puede ser que la introduzcamos en la de submissions
        '''

        data = self.submissions(cik)
        forms = pd.DataFrame.from_dict(data['filings']['recent'])
        return forms
    
    def companyconcept(self, cik: str):
        response = requests.get(
        self.BASE_URL + f'api/xbrl/companyconcept/CIK{cik}.json',
        headers = self.headers)
        data = json.loads(response.text)
        pass

    def companyfacts(self, cik: str):
        response = requests.get(
        self.BASE_URL + f'api/xbrl/companyfacts/CIK{cik}.json',
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

    def frames(self, cik: str):
        pass