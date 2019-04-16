# nba-scraper

##### A Python API for pulling data from [Basketball-reference.com](https://www.basketball-reference.com/). 

Data is scraped, compiled, cleansed, and returned in a neat table (Pandas DataFrame) ready for analysis. No signup or API keys required.

### Dependencies:
 - pandas
 - requests_HTML

### Usage:

```python

from nba_scraper.get_data import get_players_advanced_stats

#get the latest advanced player stats as a Pandas DataFrame
players = get_players_advanced_stats()

#get a specific list of player stats (not case sensitive)
players = get_players_advanced_stats(players=['Lebron James','james harden', 'Chandler Hutchison'])

#get a specific season, by season's end year
players = get_players_advanced_stats(year=2012)
```

### Output Example:

```python
#show the first 5 rows of the players DataFrame
players.head()
```
```
   ranker         player pos   age team_id  ...   bpm-dum  obpm  dbpm   bpm  vorp
0     1.0    Jeff Adrien  PF  25.0     HOU  ...       0.0  -5.4  -2.3  -7.7  -0.1
1     2.0  Arron Afflalo  SG  26.0     DEN  ...       0.0   2.5  -1.6   0.8   1.5
2     3.0   Blake Ahearn  PG  27.0     UTA  ...       0.0 -10.3  -6.0 -16.3  -0.1
3     4.0  Solomon Alabi   C  23.0     TOR  ...       0.0  -5.6   1.5  -4.1  -0.1
4     5.0   Cole Aldrich   C  23.0     OKC  ...       0.0  -2.4   2.7   0.3   0.1
```


### Easily Export to CSV:

```python
#return a df, as well as export the data to csv
players = get_players_advanced_stats(csv=True)
```


### Other Functions currently available:

```python
from nba_scraper.get_data import get_games, get_team_per_game_stats


#returns all team aggregated stats for a given season
teams = get_team_per_game_stats(year=2019)
```

### Current Work In Progress:
 - nba_scraper.get_data.get_games



