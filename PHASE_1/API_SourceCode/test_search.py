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
