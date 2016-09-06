from flask import g
from sqlalchemy import *

def retrieve_posts(tid, author_id, limit_multiplier, g, forum_post):
	posts = []
	limit_multiplier_as_int = int(limit_multiplier)
	author_id_as_int = int(author_id)
	tid_as_int = int(tid)

	if author_id_as_int == -1:
		sql_command = 'SELECT pid, fid, tid, author, authorid, subject, dateline, message FROM %s WHERE tid = %s ORDER BY dateline ASC LIMIT %s' % (forum_post, '%s', 40 * limit_multiplier_as_int)
	else:
		sql_command = 'SELECT pid, fid, tid, author, authorid, subject, dateline, message FROM %s WHERE tid = %s AND authorid = %s ORDER BY dateline ASC LIMIT %s' % (forum_post, '%s', author_id_as_int, 40 * limit_multiplier_as_int)

	cur = g.conn.execute(sql_command, tid)
	result_list = cur.fetchall()
	for result in result_list:
		post_info = {}
		post_info['pid'] = result[0]
		post_info['fid'] = result[1]
		post_info['tid'] = result[2]
		post_info['author'] = result[3]
		post_info['author_id'] = result[4]
		post_info['subject'] = result[5]
		post_info['dateline'] = result[6]
		post_info['message'] = result[7]

		posts.append(post_info)

	return posts 