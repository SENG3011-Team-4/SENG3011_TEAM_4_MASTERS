from database import *
import re
class InputError(HTTPException):
	code = 400
	message = 'Input Error'
def auth_register_v1(username, email, password):

	# check if email is valid
	if not(re.search(VALID_EMAIL, email)):
		raise InputError(description='Invalid email address')

	# check if the email is used by another user
	find_user_by_email(email)
	if find_user_by_email(email) != None:
	raise InputError(
	    description='This email is associated with another account')

	# check invalid password
	if (len(password) < 8):
		raise InputError(description='Length of password too short')

	# if input username
	if not (len(username) in range(1, 20)):
		raise InputError(description='Invalid username')

	# store info of this user
	uid = len(existing_emails) + 1


	token = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')
	record_user = {
		"usernamd":username,
		"email":email,
		"password":password,
		"u_id":u_id
	}
	registed_user(record_user)
	Session_user = {
		"u_id":u_id
		"token":token
	}
	Session_update(Session_user)
	return {
	'token': token,
	'uid': uid
	    }
def auth_login_v1(email, password):

	# connect to database

	# check if email is valid
	if not(re.search(VALID_EMAIL, email)):
		raise InputError(description='Invalid email address')

	login_info = find_user_by_email(email)
	if login_info == None:
		raise InputError(description='The email is not registered')


	# incorrect password
	if (login_info["password"] != password):
		raise InputError(description='The password entered is incorrect')
	# successful login
	uid = user["u_id"]
	token = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')
	
	Session_user = {
		"u_id":u_id
		"token":token
	}
	Session_update(Session_user)
	return {
	'token': token,
	'uid': uid
	}
def auth_logout_v1(token):


    is_success = False
    check_session_by_token(token)
    
    #print(token_record)
    if check_session_by_token is None:
        raise AccessError(description='invalid token')
    else:
        #delete this user from session db
        is_success = True

    return {'is_success': is_success}
