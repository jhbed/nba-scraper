from requests_html import HTMLSession
import pandas as pd  
import datetime as dt
from .util import  export_to_csv
from .scrapers import scrape_url_for_table

def get_players_advanced_stats(year=None, csv=None, playernames=None):
    '''
    
    returns primary player season aggregated stats in a pandas dataframe

    Inputs: 
        url (str) - the url that the desired table lives. If none, url is supplied internally
        year (int) - year desired, if none, current year is supplied
        csv (bool) - csv desired
    Outputs:
        players (DataFrame Object) - a pandas dataframe that holds all current NBA players and their advanced stats
    '''

    df = scrape_url_for_table(internal_url='https://www.basketball-reference.com/leagues/NBA_{}_advanced.html', 
                              url=None, 
                              year=year, 
                              table_selector='table#advanced_stats', 
                              non_numeric_columns=['player', 'pos', 'team_id'], 
                              csv=csv)

    if playernames is not None:
        playernames = [name.lower() for name in playernames]
        df = df[df.player.str.lower().isin(playernames)]
    return df



def get_team_per_game_stats(year=None, csv=None):
    '''
    TODO: Append oppenent stats on the end of this dataframe

    Returns primary per game stats for each time in a pandas dataframe

    Inputs: 
        url (str) - the url that the desired table lives. If none, url is supplied internally
        year (int) - year desired, if none, current year is supplied
        csv (bool) - csv desired
    Outputs:
        team_game_stats (DataFrame Object) - a pandas dataframe that holds the desired game stats for given year for all teams
    '''

    df = scrape_url_for_table(internal_url='https://www.basketball-reference.com/leagues/NBA_{}.html', 
                              url=None, 
                              year=year, 
                              table_selector='table#team-stats-per_game', 
                              non_numeric_columns=['team_name'], 
                              csv=csv)
    return df

def get_games(year=None, csv=None, verbose=False):

    months_in_season = ['october', 
                        'november', 
                        'december',
                        'january',
                        'february',
                        'march',
                        'april',
                        'may',
                        'june']
    all_urls = []
    df_all = None
    for month in months_in_season:
        if verbose:
            print('parsing: ', month)

        url = f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html'
        df, urls = scrape_url_for_table(internal_url=url, 
                                  url=None, 
                                  year=year, 
                                  table_selector='table#schedule', 
                                  non_numeric_columns=None, 
                                  csv=False,
                                  fillna=False,
                                  url_field='box_score_text')
        if df_all is None:
            df_all = df
        else:
            df_all = df_all.append(df)

        all_urls.extend(urls)

    df_all.reset_index(drop=True, inplace=True)
    df_all['url'] = pd.Series(all_urls)

    if csv:
        export_to_csv(df_all, year)
    
    return df_all

    # main_url = 'https://www.basketball-reference.com'
    # for url in urls:
    #   full_url = main_url + url 
    #   print(full_url)










