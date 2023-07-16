# easysec
Python library to import data from SEC.gov

Install via pip: ```pip install easysec```

Example usage
```
import easysec

# Define the user agent headers as a dict
headers = {'User-Agent': "email@address.com"}

# To get all companies tickers and basic data
easysec = easysec(headers)
companytickers = easysec.companytickers()
companytickers

# To the following functions is needed to set the company with an specific CIK
easysec.set_company('0000789019')

# Company data
companydata = easysec.companydata()

# Submissions
submissions = easysec.submissions()

# Company concept
companyconcept = easysec.companyconcept('AccountsPayableCurrent')

# Company facts
companyfacts = easysec.companyfacts()

# Frames
frames = easysec.frames('AccountsPayableCurrent', 'USD', 'CY2019Q1I')
```

### Company tickers
Set the CIK (Central Index Key) of the company.

Args:
    cik (str): Central Index Key (CIK) of the company.

### Company data
Retrieve data for the specified company.

Returns:
    pd.DataFrame: DataFrame containing company data.

Raises:
    ValueError: If CIK is not specified with set_company().

### Submissions
Retrieve recent submissions for the specified company.

Returns:
    pd.DataFrame: DataFrame containing recent submissions.

Raises:
    ValueError: If CIK is not specified with set_company().

### Company concept
Retrieve company concept data for the specified concept.

Args:
    concept (str): Concept name.

Returns:
    pd.DataFrame: DataFrame containing company concept data.

Raises:
    ValueError: If CIK is not specified with set_company().

### Company facts
Retrieve company facts for the specified company.

Returns:
    pd.DataFrame: DataFrame containing company facts.

Raises:
    ValueError: If CIK is not specified with set_company().

### Frames
Retrieve frames data for the specified tag, unit of measure (uom), and calculation context (ccp).

Args:
    tag (str): XBRL tag.
    uom (str): Unit of measure.
    ccp (str): Calculation context.

Returns:
    pd.DataFrame: DataFrame containing frames data.