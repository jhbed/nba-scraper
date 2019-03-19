from requests_html import HTMLSession
import pandas as pd  
import datetime as dt
from .util import scrape_url_for_table

def get_players_advanced_stats(url=None, year=None, csv=None, playernames=None):
	'''
	Inputs: 
		url (str) - the url that the desired table lives. If none, url is supplied internally
		year (int) - year desired, if none, current year is supplied
		csv (bool) - csv desired
	Outputs:
		players (DataFrame Object) - a pandas dataframe that holds all current NBA players and their advanced stats
	'''

	df = scrape_url_for_table(internal_url='https://www.basketball-reference.com/leagues/NBA_{}_advanced.html', 
		                      url=url, 
		                      year=year, 
		                      table_selector='table#advanced_stats', 
		                      non_numeric_columns=['player', 'pos', 'team_id'], 
		                      csv=csv)

	if playernames is not None:
		playernames = [name.lower() for name in playernames]
		df = df[df.player.str.lower().isin(playernames)]
	return df



def get_team_per_game_stats(url=None, year=None, csv=None):
	'''
	Inputs: 
		url (str) - the url that the desired table lives. If none, url is supplied internally
		year (int) - year desired, if none, current year is supplied
		csv (bool) - csv desired
	Outputs:
		team_game_stats (DataFrame Object) - a pandas dataframe that holds the desired game stats for given year for all teams
	'''

	df = scrape_url_for_table(internal_url='https://www.basketball-reference.com/leagues/NBA_{}.html', 
		                      url=url, 
		                      year=year, 
		                      table_selector='table#team-stats-per_game', 
		                      non_numeric_columns=['team_name'], 
		                      csv=csv)
	return df








