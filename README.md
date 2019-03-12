# nba-scraper

An API for pulling datasets from Basketball-reference.com

### Usage:

```python

from nba_scraper.players import get_players_advanced_stats

#get the latest advanced player stats as a Pandas DataFrame
players = get_players_advanced_stats()

#get a specific year
players = get_players_advanced_stats(year=2012)

#type in your own url (must be a valid player table url)
players = get_players_advanced_stats(url='https://www.basketball-reference.com/leagues/NBA_2019_advanced.html')

#return a df, as well as export the data to csv
players = get_players_advanced_stats(csv=True)
