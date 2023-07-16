import requests
import json
import pandas as pd

class easysec():
    BASE_URL = 'https://data.sec.gov/'

    def __init__(self, headers: dict, cik = None):
        """
        Constructor method for the easysec class.
        
        Args:
            headers (dict): HTTP headers for making requests.
            cik (str, optional): Central Index Key (CIK) of the company. Defaults to None.
        """
        self.headers = headers
        self.cik = None

    def companytickers(self):
        """
        Retrieve a list of company tickers from the SEC.
        
        Returns:
            pd.DataFrame: DataFrame containing company tickers and CIKs.
        """
        # Make an HTTP GET request to the SEC's company_tickers.json endpoint
        response = requests.get(
            'https://www.sec.gov/files/company_tickers.json',
            headers = self.headers)
        data = json.loads(response.text)
        df = pd.DataFrame.from_dict(data, orient='index')
        df['cik_str'] = df['cik_str'].astype(str).str.zfill(10)
        return df

    def set_company(self, cik: str):
        """
        Set the CIK (Central Index Key) of the company.

        Args:
            cik (str): Central Index Key (CIK) of the company.
        """
        self.cik = cik.zfill(10)
    
    def companydata(self):
        """
        Retrieve data for the specified company.

        Returns:
            pd.DataFrame: DataFrame containing company data.
        
        Raises:
            ValueError: If CIK is not specified with set_company().
        """
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
        """
        Retrieve recent submissions for the specified company.

        Returns:
            pd.DataFrame: DataFrame containing recent submissions.
        
        Raises:
            ValueError: If CIK is not specified with set_company().
        """
        if self.cik == None:
            raise ValueError('You must specify a CIK code.')
        response = requests.get(
            self.BASE_URL + f'submissions/CIK{self.cik}.json',
            headers = self.headers)
        data = json.loads(response.text)

        df = pd.DataFrame.from_dict(data['filings']['recent'])

        return df

    def companyconcept(self, concept):
        """
        Retrieve company concept data for the specified concept.

        Args:
            concept (str): Concept name.

        Returns:
            pd.DataFrame: DataFrame containing company concept data.
        
        Raises:
            ValueError: If CIK is not specified with set_company().
        """
        if self.cik == None:
            raise ValueError('You must specify a CIK code.')
        response = requests.get(
            self.BASE_URL + f'api/xbrl/companyconcept/CIK{self.cik}/us-gaap/{concept}.json',
            headers = self.headers)
        data = json.loads(response.text)

        units = [*data['units'].keys()]

        dfs_units = list()
        for unit in units:
            temp_df = pd.json_normalize(data, ['units', [unit]])
            temp_df.insert(0, 'unit', unit)
            dfs_units.append(temp_df)
        
        df = pd.concat(dfs_units)
        df.reset_index(inplace=True)

        return df

    def companyfacts(self):
        """
        Retrieve company facts for the specified company.

        Returns:
            pd.DataFrame: DataFrame containing company facts.
        
        Raises:
            ValueError: If CIK is not specified with set_company().
        """
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
        """
        Retrieve frames data for the specified tag, unit of measure (uom), and calculation context (ccp).

        Args:
            tag (str): XBRL tag.
            uom (str): Unit of measure.
            ccp (str): Calculation context.

        Returns:
            pd.DataFrame: DataFrame containing frames data.
        """
        response = requests.get(
            self.BASE_URL + f'api/xbrl/frames/us-gaap/{tag}/{uom}/{ccp}.json',
            headers = self.headers)
        data = json.loads(response.text)

        meta = [*data.keys()]
        meta.remove('data')

        df = pd.json_normalize(data, 'data', meta)

        return df
