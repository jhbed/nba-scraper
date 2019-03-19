from requests_html import HTMLSession
import pandas as pd  
import datetime as dt


def get_year_and_url(year, url_passed, url_internal):

	if year is None:
		year = dt.datetime.now().year

	if url_passed is None:
		url_passed = url_internal.format(year)

	return year, url_passed

def parse_table(selector):
	'''
	Inputs: 
		selector (requests-HTML html Object) - an HTML object that can be searched
	Outputs:
		table (dict) - a dictionary of lists representing columns of data
	'''
	html_table = selector.find('tbody', first=True)
	thead = selector.find('thead', first=True).find('tr', first=True)

	headings = [heading.attrs['data-stat'] for heading in thead.find('th')]

	rows = html_table.find('tr')
	table = {}

	for heading in headings:
	    table[heading] = []
	    
	for row in rows:
	    try:
	        ranker = row.find('th', first=True).text
	        
	        if ranker == 'Rk':
	             continue
	                
	        cols = row.find('td')        
	        table['ranker'].append(ranker)
	        for col in cols:
	            heading = col.attrs['data-stat']
	            table[heading].append(col.text)
	                   
	    except Exception as e:
	        print(e)

	return table

def scrape_url_for_table(internal_url, url, year, table_selector, non_numeric_columns, csv):
	'''
	Inputs: 
		internal_url (str) - an interpolateable url that is used by default if url is not provided
		url (str) - the user provided url
		year (int) - desired year for the data
		table_selector (str) - the unique html selector for the table
		non_numberic_columns (list<str>) - a list of column names that are not-numeric in the output table (hopefully deprecated soon)
		csv (bool) - whether or not a csv file output is desired. If true a csv will be created 
	Outputs:
		df (DataFrame object) - a cleaned pandas dataframe with the desired data
	'''
	year, url = get_year_and_url(year, url, internal_url)

	session = HTMLSession()
	r = session.get(url)
	#on first run this will trigger chromium/pyppeteer download
	r.html.render()

	html_table = r.html.find(table_selector,first=True)
	table = parse_table(html_table)
	df = pd.DataFrame(table)

	df = df.replace('', '0')
	df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna('0'))
	for col in df:
		if col not in non_numeric_columns:
			df[col] = df[col].astype(float)


	if csv:
		now = dt.datetime.now()
		now = now.strftime('%Y%m%d')
		df.to_csv(f'df_{year}_season_extracted_{now}.csv')

	return df