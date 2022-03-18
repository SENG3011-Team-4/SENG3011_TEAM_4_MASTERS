import sys
sys.path.append("..")
from API_SourceCode.Search import *
import pytest
import re

def test_search_v1():
	
	#with pytest.raises(ValueError):
	#	search_v1("anything","United state","2002-01-01T01:01:01","2000-01-01T01:01:01",Timezone = "UTC")
		
	with pytest.raises(ValueError):
		search_v1("anything","United state","1","2",Timezone = "UTC")

def test_timezone():
	assert Check_Timezone("2020-05-02T15:12:12", "UTC+03:00") == "2020-05-02T12:12:12"
	assert Check_Timezone("2020-05-02T15:12:12", "UTC-03:00") == "2020-05-02T18:12:12"
	with pytest.raises(ValueError):
		Check_Timezone("2020-05-02T15:12:12", "something random")
