from flask import g
from sqlalchemy import *

def retrieve_threads(fid, limit_multiplier, g, forum_threads):
	threads = []

	sql_command = 'SELECT tid, fid, typeid, sortid, author, authorid, CONVERT(subject USING utf8), dateline, lastposter, views, replies FROM %s WHERE fid = %s ORDER BY dateline DESC LIMIT %s  ' % (forum_threads, '%s', 40 * limit_multiplier)

	cur = g.conn.execute(sql_command, fid)
	result_list = cur.fetchall()
	for result in result_list:
		thread_info = {}
		thread_info['tid'] = result[0]
		thread_info['fid'] = result[1]
		thread_info['type_id'] = result[2]
		thread_info['sort_id'] = result[3]
		thread_info['author'] = result[4]
		thread_info['authorid'] = result[5]
		thread_info['subject'] = result[6]
		thread_info['dateline'] = result[7]
		thread_info['lastposter'] = result[8]
		thread_info['views'] = result[9]
		thread_info['replies'] = result[10]

		threads.append(thread_info)

	return threads
