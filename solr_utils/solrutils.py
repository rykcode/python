#/usr/local/bin/python3
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import config

# code snippet to deep page through solr search results



def deeppage(solr_url, query, fields, batch_size_requested=500):
    '''
    Provides a generator over solr query result list using solr deep-paging.
    If the data for machine learning is stored in solr then using this function
    you can load the data in to a desired data structure such as pandas.
    Parameters:
        -----------
        solr_url: str
            The solr url including the port and index name.
        query: str
            The solr query
        fields: str
            comma separated list of solr fields to return
        batch_size: int
            Batch size or Page size for deep paging
    Returns:
        Returns a generator over the solr query result
    Usage:
        -----------
        query = 'from_name_s:"Mark E Haedicke"'
        fields = 'uuid_s,from_name_s,from_address_s,to_address_ss,sent_time_dt'
        solr_url = 'http://localhost:8983/demo/select'
        for docs_batch in deeppage(solr_url=solr_url, query=query, fields=fields):
            print ('%s' % docs_batch)

    '''
    cursor_mark = '*'
    payload = {
                'q': query, 
                'wt': 'json',
                'fl': fields,
                "sort":"id asc",
                'cursorMark': cursor_mark,
                'rows' : str(batch_size_requested),
                }
    r = requests.get(solr_url, data=payload)
    next_cursor_mark = r.json()['nextCursorMark']
    num_found = r.json()['response']['numFound']
    docs_batch = r.json()['response']['docs']
    print('num_found:%d' % num_found)
    while next_cursor_mark != cursor_mark:
        docs_batch = r.json()['response']['docs']
        print('len(docs_batch):%d' % len(docs_batch))
        cursor_mark = next_cursor_mark
        payload['cursorMark'] = cursor_mark
        r = requests.get(solr_url, data=payload)
        next_cursor_mark = r.json()['nextCursorMark']
        print('cursor marks:%s, %s' % (cursor_mark, next_cursor_mark))
        yield docs_batch

def create_df(solr_url, query, fields, batch_size=500):
    '''
    Create a pandas dataframe from the results of the solr query
    Parameters:
        -----------
        solr_url: str
            The solr url including the port and index name.
        query: str
            The solr query
        fields: str
            comma separated list of solr fields to return
        batch_size: int (Default 500)
            Batch size or Page size for deep paging
    Returns:
        Returns a pandas dataframe, 
        num_rows = size of search result, num_cols = num fields requested
    Usage:
        -----------
        query = 'from_name_s:"Mark E Haedicke"'
        fields = 'uuid_s,from_name_s,from_address_s,to_address_ss,sent_time_dt'
        solr_url = 'http://localhost:8983/demo/select'
        df = create_df(solr_url, query, fields)
        print(df.head())
    '''
    docs_list = []
    for docs_batch in deeppage(solr_url=solr_url, query=query, fields=fields):
        docs_list += docs_batch
    df = pd.DataFrame(docs_list)
    return df

