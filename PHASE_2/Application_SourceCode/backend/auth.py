from http.client import HTTPException
from database import *
from fastapi import HTTPException
import hashlib
import re
import jwt

SECRET = "Seng3011Team4"

class InputError(HTTPException):
	code = 400
	message = 'Input Error'

class AccessError(HTTPException):
	code = 403
	message = 'Access Error'

def auth_register_v1(username, email, password):

	# check if email is valid
	if not(re.search('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email)):
		raise HTTPException(status_code = 400, detail='Invalid Email or Password')
	if find_user_by_email(email) != None:
		raise HTTPException(status_code = 400, detail='Invalid Email or Password')
    # check invalid password

	if (len(password) < 8):
		raise HTTPException(status_code = 400, detail='Invalid Email or Password')

	# if input username
	if not (len(username) in range(1, 20)):
		raise HTTPException(status_code = 400, detail='Invalid Email or Password')

	# store info of this user
	lenth = 0
	for i in user_list():
		lenth=lenth+1
	u_id = lenth + 1

	#encode password
	password = hashlib.sha256(password.encode()).hexdigest()#encode password
	token = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')

	record_user = {
		"usernamd":username,
		"email":email,
		"password":password,
		"u_id":u_id
	}
	
	registered_user(record_user)

	session_user = {
		"u_id":u_id,
		"token":token
	}
	
	session_update(session_user)
	
	return {
		'token': token,
		'uid': u_id
	}

def auth_login_v1(email, password):

	# connect to database
	login_info = find_user_by_email(email)
	if login_info == None:
		raise HTTPException(status_code = 401, detail='Incorrect Email or Password')

	password = hashlib.sha256(password.encode()).hexdigest()
	# incorrect password
	if (login_info["password"] != password):
		raise HTTPException(status_code = 401, detail='Incorrect Email or Password')
	
	# successful login
	u_id = login_info["u_id"]
	token = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')
	
	session_user = {
		"u_id":u_id,

		"token":token
	}

	session_update(session_user)
	
	return {
		'token': token,
		'uid': u_id
	}

def auth_logout_v1(token):

	check = check_session_by_token(token)

	if check is None:
		raise HTTPException(status_code = 400, detail='Logout Failed')
	else:
		delete_session(token)

	return {
		'is_success': True
	}

