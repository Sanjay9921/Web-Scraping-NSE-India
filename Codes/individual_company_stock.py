from io import StringIO
import requests
import pandas as pd
from  datetime import datetime , timedelta
import bs4

session = requests.session()

head = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.88 Safari/537.36 "
}


def getHistoryData(company, from_date=(datetime.today().strftime("%d-%m-%Y")), to_date=(datetime(datetime.today().year - 1, datetime.today().month,datetime.today().day).strftime("%d-%m-%Y"))):
    #All URLs
    website_url = "https://www.nseindia.com"
    get_website_url = "https://www.nseindia.com/get-quotes/equity?symbol="
    get_website_historical_url = "https://www.nseindia.com/api/historical/cm/equity?symbol="
    
    session.get(website_url, headers=head)
    session.get(get_website_url + company, headers=head)  # to save cookies
    session.get(get_website_historical_url+company, headers=head)
    url = get_website_historical_url + company + "&series=[%22EQ%22]&from=" + from_date + "&to=" + to_date + "&csv=true"
    webdata = session.get(url=url, headers=head)
    df = pd.read_csv(StringIO(webdata.text[3:]))
    return df

def niftyHistoryData(varient, from_date = ((datetime(datetime.today().year - 1, datetime.today().month, datetime.today().day) + timedelta(days=2)).strftime("%d-%m-%Y")), to_date =(datetime.today().strftime("%d-%m-%Y"))):
    #Varient Example: 'NIFTY 50'
    varient = varient.upper()
    varient = varient.replace(' ', '%20')
    varient = varient.replace('-', '%20')
    
    #NIFTY URL
    nifty_url = "https://www1.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp?indexType="
    webData = session.get(url= nifty_url + varient + "&fromDate=" + from_date + "&toDate=" + to_date, headers=head)
    soup = bs4.BeautifulSoup(webData.text, 'html5lib')
    return pd.read_csv(StringIO(soup.find('div', {'id': 'csvContentDiv'}).contents[0].replace(':','\n')))