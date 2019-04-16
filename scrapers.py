from requests_html import HTMLSession
import pandas as pd  
import datetime as dt
from .util import get_year_and_url, export_to_csv



def parse_table(selector, url_field=None):
    '''
    Inputs: 
        selector (requests-HTML html Object) - an HTML object that can be searched
    Outputs:
        table (dict) - a dictionary of lists representing columns of data
    '''
    urls = []
    html_table = selector.find('tbody', first=True)
    thead = selector.find('thead', first=True).find('tr')[-1]

    headings = [heading.attrs['data-stat'] for heading in thead.find('th')]

    rows = html_table.find('tr')
    table = {}

    for heading in headings:
        table[heading] = []
        
    for row in rows:
        try:
            ranker = row.find('th', first=True)
            ranker_ident = ranker.attrs['data-stat']
            
            if ranker.text in ['Rk', 'Reserves']:
                 continue
                    
            cols = row.find('td')        
            table[ranker_ident].append(ranker.text)


            for col in cols:
                heading = col.attrs['data-stat']

                if heading == 'reason':
                    del table[ranker_ident][-1]
                    continue

                table[heading].append(col.text)

                if url_field is not None:
                    if heading == url_field:
                        urls.append(col.find('a', first=True).attrs['href'])
                       
        except Exception as e:
            try:
                th = row.find('th', first=True).text
                if th == 'Playoffs':
                    continue
                else:
                    caption = selector.find('caption', first=True).text
                    print('error parsing ', caption)
                    print(e)
            except:
                print('looks like there is no valid table for the selector given')
                print(e)

    return table, urls


def scrape_url_for_table(internal_url, 
                         url, 
                         year, 
                         table_selector, 
                         non_numeric_columns, 
                         csv, 
                         fillna=True,
                         url_field=None,
                         scraper_func=None):
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
    table, urls = parse_table(html_table, url_field)
    df = pd.DataFrame(table)

    if fillna:
        df = df.replace('', '0')
        df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna('0'))
        for col in df:
            if col not in non_numeric_columns:
                df[col] = df[col].astype(float)


    if csv:
        export_to_csv(df, year)

    
    if url_field:
        return df, urls
    else:
        return df