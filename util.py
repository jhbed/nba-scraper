from requests_html import HTMLSession
import pandas as pd  
import datetime as dt


def export_to_csv(df, year):
    now = dt.datetime.now()
    now = now.strftime('%Y%m%d')
    df.to_csv(f'df_{year}_season_extracted_{now}.csv')


def get_year_and_url(year, url_passed, url_internal):

    if year is None:
        year = dt.datetime.now().year

    if url_passed is None:
        url_passed = url_internal.format(year)

    return year, url_passed

