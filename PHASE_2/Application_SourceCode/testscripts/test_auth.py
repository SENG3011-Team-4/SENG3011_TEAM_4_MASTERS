from database import *
from search import *
from auth import *
import pytest

def test_register_invalid_email():
	toggleTests(True)
	clearAll()
	with pytest.raises(InputError):
		auth_register_v1('user1', 'invalid.com', 'password')
	with pytest.raises(InputError):
		auth_register_v1('user1', 'invalidemail@', 'password')
	toggleTests(False)

def test_register_used_email():
	toggleTests(True)
	clearAll()
	auth_register_v1('user1', 'user@outlook.com', 'password')
	with pytest.raises(InputError):
		auth_register_v1('user2', 'user@outlook.com', 'password')
	toggleTests(False)
	
def test_register_invalid_password():
	toggleTests(True)
	clearAll()
	with pytest.raises(InputError):
		auth_register_v1('user1', 'reguser1@outlook.com', '1234567')
	with pytest.raises(InputError):
		auth_register_v1('user1', 'reguser2@outlook.com', 'short')
	toggleTests(False)

def test_register_invalid_username():
	toggleTests(True)
	clearAll()

	with pytest.raises(InputError):
		auth_register_v1('user1haveaverlongusername', 'reguser1@outlook.com', 'password')
	with pytest.raises(InputError):
		auth_register_v1('', 'reguser2@outlook.com', 'password')
	toggleTests(False)

def test_register_valid():
	toggleTests(True)
	clearAll()
	register_result = auth_register_v1('user1', 'reguser1@outlook.com', 'password')
	login_result = auth_login_v1('reguser1@outlook.com', 'password')
	assert (register_result['uid'] == login_result['uid'])
	toggleTests(False)

def test_login_invalid_email():
	toggleTests(True)
	clearAll()
	auth_register_v1('user1', 'reguser1@outlook.com', 'password')
	auth_register_v1('user2', 'reguser2@outlook.com', 'password')
	with pytest.raises(InputError):
		auth_login_v1('invalid.com', 'password')
	with pytest.raises(InputError):
		auth_login_v1('invalidemail@', 'password')
	toggleTests(False)

def test_login_not_registed_email():
	toggleTests(True)
	clearAll()
	auth_register_v1('user1', 'reguser1@outlook.com', 'password')
	with pytest.raises(InputError):
		auth_login_v1('unknowemail@outlook.com', 'password')
	toggleTests(False)

def test_login_incorrect_password():
	toggleTests(True)
	clearAll()
	auth_register_v1('user1', 'reguser1@outlook.com', 'password')
	with pytest.raises(InputError):
		auth_login_v1('reguser1@outlook.com', 'wrongpassword')
	toggleTests(False)

def test_register_and_login_valid():
	toggleTests(True)
	clearAll()
	register_result = auth_register_v1('user1', 'reguser1@outlook.com', 'password')
	login_result = auth_login_v1('reguser1@outlook.com', 'password')
	assert (register_result['uid'] == login_result['uid'])     	
	toggleTests(False)

def test_logout_invalid_token():
	toggleTests(True)
	clearAll()
	auth_register_v1('user1', 'reguser1@outlook.com', 'password')
	login_result = auth_login_v1('reguser1@outlook.com', 'password')
	invalid_token = "123456"   	
	with pytest.raises(AccessError):
		auth_logout_v1(invalid_token)
	toggleTests(False)

def test_logout_valid():
	toggleTests(True)
	clearAll()
	auth_register_v1('user1', 'reguser1@outlook.com', 'password')
	login_result = auth_login_v1('reguser1@outlook.com', 'password')
	assert auth_logout_v1(login_result["token"]) == {'is_success': True}
	with pytest.raises(AccessError):
		auth_logout_v1(login_result["token"])
	toggleTests(False)
        	
