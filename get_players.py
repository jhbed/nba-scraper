from requests_html import HTMLSession
import pandas as pd  
import datetime as dt

def get_players(url=None, year=None):
	'''
	Inputs: 
		url - the url that the players table lives. If none, return the current players
	Outputs:
		players - a pandas dataframe that holds all current NBA players and their advanced stats
	'''
	if year is None:
		year = dt.datetime.now().year

	if url is None:
		url = f'https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html'

	session = HTMLSession()
	r = session.get(url)

	advanced_stats = r.html.find('table',first=True)
	html_table = advanced_stats.find('tbody', first=True)
	thead = advanced_stats.find('thead', first=True).find('tr', first=True)

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
	            #print('found: ', col.text)
	            table[heading].append(col.text)
	                   
	    except Exception as e:
	        print(e)

	players = pd.DataFrame(table)
	return players

