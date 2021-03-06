from database import *
from Search import *
from auth import *
import pytest
def test_register_invalid_email():

	with pytest.raises(InputError):
        	auth_register_v1('user1', 'invalid.com', 'password')
    	with pytest.raises(InputError):
        	auth_register_v1('user1', 'invalidemail@', 'password')

def test_register_used_email():

	auth_register_v1('user1', 'user@outlook.com', 'password')
    	with pytest.raises(InputError):
        	auth_register_v1('user2', 'user@outlook.com', 'password')
        	
def test_register_invalid_password():

	with pytest.raises(InputError):
		auth_register_v1('user1', 'reguser1@outlook.com', '1234567')
	with pytest.raises(InputError):
		auth_register_v1('user1', 'reguser2@outlook.com', 'short')

def test_register_invalid_username()


	with pytest.raises(InputError):
		auth_register_v1('user1haveaverlongusername', 'reguser1@outlook.com', 'password')
	with pytest.raises(InputError):
		auth_register_v1('', 'reguser2@outlook.com', 'password')

def test_register_valid():

	register_result = auth_register_v1('user1', 'reguser1@outlook.com', 'password')
    	login_result = auth_login_v1('reguser1@outlook.com', 'password')
    	assert (register_result['uid'] == login_result['uid'])
def test_login_invalid_email():

	auth_register_v1('user1', 'reguser1@outlook.com', 'password')
	auth_register_v1('user2', 'reguser2@outlook.com', 'password')
	with pytest.raises(InputError):
        	auth_login_v1('invalid.com', 'password')
    	with pytest.raises(InputError):
        	auth_login_v1('invalidemail@', 'password')

def test_login_not_registed_email():

	auth_register_v1('user1', 'reguser1@outlook.com', 'password')
	with pytest.raises(InputError):
        	auth_login_v1('unknowemail@outlook.com', 'password')
        	
def test_login_incorrect_password():

	auth_register_v1('user1', 'reguser1@outlook.com', 'password')
	with pytest.raises(InputError):
        	auth_login_v1('reguser1@outlook.com', 'wrongpassword')
        	
def test_register_and_login_valid():

	register_result = auth_register_v1('user1', 'reguser1@outlook.com', 'password')
    	login_result = auth_login_v1('reguser1@outlook.com', 'password')
    	assert (register_result['uid'] == login_result['uid'])     	
  
def test_logout_invalid_token():
	auth_register_v1('user1', 'reguser1@outlook.com', 'password')
    	login_result = auth_login_v1('reguser1@outlook.com', 'password')
    	invalid_token = str(login_result['token']) + 'fj2'   	
	with pytest.raises(AccessError):
        	auth_logout_v1(invalid_token)

def test_logout_valid():
	auth_register_v1('user1', 'reguser1@outlook.com', 'password')
    	login_result = auth_login_v1('reguser1@outlook.com', 'password')
	assert auth_logout_v1(login_result["token"]) == {'is_success': True}
	with pytest.raises(AccessError):
        	auth_logout_v1(login_result["token"])
        	
        	
