from flask import g
from sqlalchemy import *

def retrieve_section_info(related_forum_ids, g, forum_sections):
	threads_info = {}
	posts_info = {}
	todayposts_info = {}

	sql_command = 'SELECT fid, threads, posts, todayposts FROM %s WHERE fid = %s' % (forum_sections, '%s')
	for id in related_forum_ids:
		cur = g.conn.execute(sql_command, id)
		result_list = cur.fetchall()
		result = result_list[0]

		threads_info[id] = result[1]
		posts_info[id] = result[2]
		todayposts_info[id] = result[3]

	# Sum up # of threads, posts and new posts today for Movie Fanfic section and TV Fanfic section
	threads_info[2] = threads_info[2] + threads_info[37] + threads_info[38]
	posts_info[2] = posts_info[2] + posts_info[37] + posts_info[38]
	todayposts_info[2] = todayposts_info[2] + todayposts_info[37] + todayposts_info[38]
	threads_info[36] = threads_info[36] + threads_info[50] + threads_info[49]
	posts_info[36] = posts_info[36] + posts_info[50] + posts_info[49]
	todayposts_info[36] = todayposts_info[36] + todayposts_info[50] + todayposts_info[49]

	return (threads_info, posts_info, todayposts_info)