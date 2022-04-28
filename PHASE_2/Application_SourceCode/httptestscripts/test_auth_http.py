import requests
import json
config = "http://54.206.19.126"
from database import *
from auth import *




def test_auth_register():
	toggleTests(True)
	clearAll()
	assert requests.post(config + '/register',
                  json={'username': 'user1', 'email': 'useremail1@gmail.com', 'password': '2h38gj20hc','name': 'user1name'}).status_code == 200
	assert requests.post(config + '/register',
                  json={'username': 'user1', 'email': 'useremail1@gmail.com', 'password': '2h38gj20hc','name': 'user1name'}).status_code == 400#already been used
	assert requests.post(config + '/register',
                  json={'username': 'user1', 'email': 'useremail1gmail.com', 'password': '2h38gj20hc', 'name': 'user1name'}).status_code == 400#invalide email
	assert requests.post(config + '/register',
                  json={'username': 'user1', 'email': 'useremail1@g', 'password': '2h38gj20hc', 'name':'user1name'}).status_code == 400#invalid email
	toggleTests(False)
	
def test_auth_register_invalid_psw():

	assert requests.post(config + '/register',
                  json={'username': 'user1', 'email': 'useremail1@gmail.com', 'password': 'short','name': 'user1name'}).status_code == 400
                  
	assert requests.post(config + '/register',
                  json={'username': 'user1', 'email': 'useremail1@gmail.com', 'password': 'toooooooooooooooooooooolong','name': 'user1name'}).status_code == 400
def test_auth_login():
	toggleTests(True)
	clearAll()
	assert requests.post(config + '/login',
                  json={ 'username': 'testuser1', 'password': '2h38gj20hc'}).status_code == 401
               
	requests.post(config + '/register',
                  json={'username': 'testuser1', 'email': 'useremail1@gmail.com', 'password': '2h38gj20hc','name': 'user1name'})
                  
	assert requests.post(config + '/login',
		  json={ 'username': 'testuser1', 'password': '2h38gj20hc'}).status_code == 401
	toggleTests(False)
def test_auth_logout_valid():
	toggleTests(True)
	clearAll()
	requests.post(config + '/register',
                  json={'username': 'testuser1', 'email': 'useremail1@gmail.com', 'password': '2h38gj20hc','name': 'user1name'})
	login_resp = requests.post(config + '/login',
                  json={ 'username': 'testuser1', 'password': '2h38gj20hc'}).status_code == 200
	payload = json.loads(login_resp.text)
               
	assert requests.post(config.url + 'logout', json={'token': payload['token']}).status_code == 200
	assert requests.post(config.url + 'logout', json={'token': 'invalid'}).status_code == 400
	toggleTests(False)
