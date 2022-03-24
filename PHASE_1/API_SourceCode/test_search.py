from database import *
from Search import *
from auth import *
import pytest
def test_search_1():
	toggleTests(True)
	clearAll()
	data_list = []
	data_1 = {
		"url": "www.example.com",
		"date_of_publication": "2018-05-02T15:12:12",
		"headline": "Outbreaks expand to Wisconsin",
		"main_text": "Avian Flu Zika sample text",
		"reports": [{
		    "diseases": [
		    "RandoVirus"
		    ],
		    "event_date": [
		    "2015-10-01T08:45:10"
		    ],
		    "locations": ["United States"]
		}]
	    }
	data_2 = {
		"url": "www.example2.com",
		"date_of_publication": "2018-05-02T15:12:12",
		"headline": "sth",
		"main_text": "sth",
		"reports": [{
		    "diseases": [
		    "Others"
		    ],
		    "event_date": [
		    "2015-10-01T08:45:10"
		    ],
		    "locations": ["United States"]
		}]
	    }
	data_list.append(data_1)
	data_list.append(data_2)
	write_report(data_list)
	search_result = search_v1("RandoVirus","United States","2015-05-02T15:12:12","2025-05-02T15:12:12")
	
	assert len(search_result["output"]) == 1
	
	assert search_result["output"][0]["url"] == data_1["url"]
	toggleTests(False)
def test_search_invalid_time():
	toggleTests(True)
	clearAll()
	with pytest.raises(ValueError):
        	search_v1("RandoVirus","United States","1","2") #invalid format
	with pytest.raises(ValueError):
        	search_v1("RandoVirus","United States","2025-05-02T15:12:12","2015-05-02T15:12:12") #start date later than end date
	with pytest.raises(ValueError):
        	search_v1("RandoVirus","United States","2015-XX-02T15:12:12","2015-05-02T15:12:12")#Unscoped
	toggleTests(False)
def test_search_fre_key_and_update():
	toggleTests(True)
	clearAll()
	search_v1("0","United States","2015-05-02T15:12:12","2025-05-02T15:12:12")
	search_v1("1","United States","2015-05-02T15:12:12","2025-05-02T15:12:12")
	search_v1("2","United States","2015-05-02T15:12:12","2025-05-02T15:12:12")
	search_v1("3","United States","2015-05-02T15:12:12","2025-05-02T15:12:12")
	search_v1("4","United States","2015-05-02T15:12:12","2025-05-02T15:12:12")
	search_v1("4","United States","2015-05-02T15:12:12","2025-05-02T15:12:12")
	search_v1("5","United States","2015-05-02T15:12:12","2025-05-02T15:12:12")
	
	
	
	assert Search_Frequently_key_v1()[0]["key"] == "4"
	assert Search_Frequently_key_v1()[0]["frequency"] == 2
	Search_Frequentlykey_update_v1("3")
	#print(Search_Frequently_key_v1())
	assert Search_Frequently_key_v1()[0]["key"] in ["3","4"]
	assert Search_Frequently_key_v1()[1]["key"] in ["3","4"]
	assert Search_Frequently_key_v1()[1]["frequency"] == 2
	toggleTests(False)
def test_Search_History():
	toggleTests(True)
	clearAll()
	usrtoken = auth_register_v1("username","useremail@gmail.com","userpassword")["token"]
	search_v1("0","United States","2015-05-02T15:12:12","2025-05-02T15:12:12",token =usrtoken )
	search_v1("1","United States","2015-05-02T15:12:12","2025-05-02T15:12:12",token =usrtoken )
	search_v1("2","United States","2015-05-02T15:12:12","2025-05-02T15:12:12",token =usrtoken )
	search_v1("3","United States","2015-05-02T15:12:12","2025-05-02T15:12:12",token =usrtoken )
	search_v1("4","United States","2015-05-02T15:12:12","2025-05-02T15:12:12",token =usrtoken )
	search_v1("4","United States","2015-05-02T15:12:12","2025-05-02T15:12:12",token =usrtoken )
	check_list = []

	for i in Search_History_v1(usrtoken):
		check_list.append(i["his"]["key_terms"])
	#print (check_list)
	assert check_list == ["4","4","3","2","1"]
	toggleTests(False)
	"""
def test_timezone():
	toggleTests(True)
	clearAll()
	assert Check_Timezone("2020-05-02T15:12:12", "UTC+03:00") == "2020-05-02T12:12:12"
	assert Check_Timezone("2020-05-02T15:12:12", "UTC-03:00") == "2020-05-02T18:12:12"
	with pytest.raises(ValueError):
		Check_Timezone("2020-05-02T15:12:12", "something random")
	toggleTests(False)
"""
if __name__ == '__main__':
	test_Search_History()
