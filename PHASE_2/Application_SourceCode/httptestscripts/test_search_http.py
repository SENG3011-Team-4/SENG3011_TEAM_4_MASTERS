import requests
import json
config = "http://54.206.19.126"
from search import *
import pandas as pd


def test_search_valid():
	
	
	assert requests.get(config + '/search',
                  params={'keyterms': 'zika', 'location': 'United states','start_date':'2015-10-01T0:45:10','end_date':'2016-10-01T0:45:10','timezone':'UTC'}).status_code == 200
	assert requests.get(config + '/search',
                  params={'keyterms': 'covid,zika', 'location': 'United states','start_date':'2015-10-01T0:45:10','end_date':'2016-10-01T0:45:10','timezone':'UTC'}).status_code == 200
def test_search_time_error():


	assert requests.get(config + '/search',
                  params={'keyterms': 'zika', 'location': 'United states','start_date':'2015-10-010:45:10','end_date':'2016-10-01T0:45:10','timezone':'UTC'}).status_code == 500
	assert requests.get(config + '/search',
                  params={'keyterms': 'zika', 'location': 'United states','start_date':'2015-10-010:45:10','end_date':'2016-10-010:45:10','timezone':'UTC'}).status_code == 500
	assert requests.get(config + '/search',
                  params={'keyterms': 'zika', 'location': 'United states','start_date':'2016-10-010:45:10','end_date':'2015-10-01T0:45:10','timezone':'UTC'}).status_code == 500
                  
def test_search_twitter_valid():
	
	
	assert requests.get(config + '/search/twitter',
                  params={'location': 'United state', 'disease': 'colds'}).status_code == 200

    #print(df_city(orient='index'))
def test_search_treatment_valid():

	assert requests.get(config + '/search/treatment', params={'disease':'colds'}).status_code == 200
	
def test_search_key_frequency_valid():
	
	assert requests.get(config + '/search/key_frequency').status_code == 200
	
def test_search_key_frequency_valid():
	
	assert requests.get(config + '/search/key_frequency').status_code == 200
