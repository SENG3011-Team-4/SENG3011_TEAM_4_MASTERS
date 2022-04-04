from database import *
from werkzeug.exceptions import HTTPException
import re
import hashlib
import jwt
import hashlib
import os.path

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
		raise InputError(description='Invalid email address')# check if the email is used by another user
	if find_user_by_email(email) != None:

		raise InputError(description='This email is associated with another account')
    # check invalid password

	if (len(password) < 8):
		raise InputError(description='Length of password too short')

	# if input username
	if not (len(username) in range(1, 20)):
		raise InputError(description='Invalid username')

	# store info of this user
	lenth = 0
	for i in user_list():
		lenth=lenth+1
	u_id = lenth + 1

	password = hashlib.sha256(password.encode()).hexdigest()#encode password
	token = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')

	record_user = {
		"usernamd":username,
		"email":email,
		"password":password,
		"u_id":u_id
	}
	registed_user(record_user)

	Session_user = {

		"u_id":u_id,

		"token":token
	}
	Session_update(Session_user)
	return {
	'token': token,

	'uid': u_id
	    }

def auth_login_v1(email, password):

	# connect to database

	# check if email is valid
	if not(re.search('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email)):
		raise InputError(description='Invalid email address')

	login_info = find_user_by_email(email)
	if login_info == None:
		raise InputError(description='The email is not registered')

	password = hashlib.sha256(password.encode()).hexdigest()
	# incorrect password
	if (login_info["password"] != password):
		raise InputError(description='The password entered is incorrect')
	# successful login
	u_id = login_info["u_id"]
	token = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')
	
	Session_user = {
		"u_id":u_id,

		"token":token
	}
	Session_update(Session_user)
	return {
	'token': token,
	'uid': u_id
	}
def auth_logout_v1(token):


    is_success = False
    check = check_session_by_token(token)
    
    #print(token_record)
    if check is None:
        raise AccessError(description='invalid token')
    else:
        delete_session(token)
        is_success = True

    return {'is_success': is_success}
    
