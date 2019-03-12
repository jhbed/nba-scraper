# nba-scraper

An API for pulling datasets from Basketball-reference.com

### Usage:

```python

from nba_scraper.get_players import get_players

#get the latest advanced player stats as a Pandas DataFrame
players = get_players()

#get a specific year
players = get_players(year=2012)

#type in your own url (must be a valid player table url)
players = get_players(url='https://www.basketball-reference.com/leagues/NBA_2019_advanced.html')
