from flask import g
from sqlalchemy import *
import hashlib

def authenticate(username, password, g, members_ucenter, member_discuz, forbidden_groups):
	authenticated_userinfo = {}

	sql_command = 'SELECT uid, username, password, email, salt FROM %s WHERE username = %s' % (members_ucenter, '%s')
	cur = g.conn.execute(sql_command, username)
	matched_user_list = cur.fetchall()

	if matched_user_list == [] or len(matched_user_list) > 1:
		return (False, authenticated_userinfo)

	matched_user = matched_user_list[0]
	fetched_password = matched_user[2]
	salt = matched_user[4]

	processed_password = process_password(password, salt)

	if processed_password != fetched_password:
		return (False, authenticated_userinfo)

	fetched_uid = matched_user[0]
	fetched_username = matched_user[1]
	
	fetched_email = matched_user[3]
	authenticated_userinfo['uid'] = fetched_uid
	authenticated_userinfo['username'] = fetched_username
	authenticated_userinfo['email'] = fetched_email
	authenticated_userinfo['groupid'] = -1

	sql_command_2 = 'SELECT groupid FROM %s WHERE uid = %s' % (member_discuz, '%s')
	cur = g.conn.execute(sql_command_2, fetched_uid)
	groupid_list = cur.fetchall()

	if groupid_list == [] or len(groupid_list) > 1:
		return (False, authenticated_userinfo)

	fetched_groupid = groupid_list[0][0]
	authenticated_userinfo['groupid'] = fetched_groupid

	if fetched_groupid in forbidden_groups:	
		return (False, authenticated_userinfo)

	return (True, authenticated_userinfo)

def process_password(password, salt):
	password_md5 = hashlib.md5(password).hexdigest()
	password_md5_withSaltString = password_md5 + salt
	password_md5_withSaltString_md5 = hashlib.md5(password_md5_withSaltString).hexdigest()
	print(password_md5_withSaltString_md5)
	return password_md5_withSaltString_md5