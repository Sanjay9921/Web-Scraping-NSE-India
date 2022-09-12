import requests

session = requests.session()

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

def getID(company_name):
    
    #All urls
    website_url = 'https://www.nseindia.com/'
    search_url = 'https://www.nseindia.com/api/search/autocomplete?q={}'
    get_details = 'https://www.nseindia.com/api/quote-equity?symbol={}'
    
    #Expect Response 200 
    session.get(website_url, headers=head)
    
    #Get all the search results of the company_name arg
    search_results = session.get(url=search_url.format(company_name), headers=head)
    
    #Get the first search result which matches the company_name user is looking for
    search_result = search_results.json()['symbols'][0]['symbol']
    
    #Get the company details from the result above
    company_details = session.get(url=get_details.format(search_result), headers=head)
    
    #Return the id of the company name
    return company_details.json()['info']['identifier']