from flask import Flask, render_template, g, request, redirect, url_for, jsonify
from sqlalchemy import *
from flask_restful import Resource, Api, reqparse
from bs4 import BeautifulSoup
import plugin_userauthentication
import plugin_search
import plugin_sectioninfo
import plugin_retrievethreads
import plugin_retrieveposts
import init_cookies
import init_res
import json
import requests
import re
import hashlib
from constants import *
import time

app = Flask(__name__)
api = Api(app)

# Set Engine for Database Access
engine = create_engine('mysql://mtSlashDevAPIAcc:mtS1ashDEVDBPass@localhost/mtSlashDevTestbedDB?charset=utf8')

# Load Settings from File
f = open('settings.config','r')
settingsInFile = f.readlines()

settings = {}

for line in settingsInFile:
	items = line.split('=')
	try:
		settings[items[0]] = int(items[1])
	except:
		settings[items[0]] = items[1]

# Initialize Cookies
cookies = init_cookies.get_cookies()

# Initialize Collection of Regular Expressions
res = init_res.get_res()

# Initialize a Parser For User Authentication 
parser_for_userauthentication = reqparse.RequestParser()
parser_for_userauthentication.add_argument('username')
parser_for_userauthentication.add_argument('password')

# Initialize a Parser for Basic Search
parser_for_basic_search = reqparse.RequestParser()
parser_for_basic_search.add_argument('keyword')
parser_for_basic_search.add_argument('page')
parser_for_basic_search.add_argument('search_id')

# Initialize a Parser for Retrieving Threads
parser_for_retrieving_threads = reqparse.RequestParser()
parser_for_retrieving_threads.add_argument('fid')
parser_for_retrieving_threads.add_argument('sort_id')
parser_for_retrieving_threads.add_argument('limit_multiplier')

# Initialize a Parser for Retrieving Posts
parser_for_retrieving_posts = reqparse.RequestParser()
parser_for_retrieving_posts.add_argument('tid')
parser_for_retrieving_posts.add_argument('author_id')
parser_for_retrieving_posts.add_argument('limit_multiplier')

# Timer for Refreshing Cached Section Info
timer_for_refreshing_cached_section_info = time.time()

# Cached Section Info
section_info = []

# Connect to Database Before a Request
@app.before_request
def before_request():
	g.conn=engine.connect()

# Disconnect from Database (if Applicable) After a Request
@app.teardown_request
def teardown_request(exception):
	if g.conn is not None:
		g.conn.close()

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/registration')
def registration():
	return render_template('registration.html')

@app.route('/usernotice')
def usernotice():
	return render_template('usernotice.html')

@app.route('/privacypolicy')
def privacypolicy():
	return render_template('privacypolicy.html')

@app.route('/whatsnew')
def whatsnew():
	return render_template('whatsnew.html')

@app.route('/userexpimprovproj')
def userexpimprovproj():
	return render_template('userexpimprovproj.html')

class CheckServerStatus(Resource):
	def get(self):
		return jsonify(**settings)

class UserAuthentication(Resource):
	def post(self):
		args = parser_for_userauthentication.parse_args()
		username = args['username']
		password = args['password']
		result = plugin_userauthentication.authenticate(username, password, g, members_ucenter, member_discuz, forbidden_groups)
		print(result[0])
		return jsonify(result = result[0], user_info = result[1])

class BasicSearch(Resource):
	def post(self):
		args = parser_for_basic_search.parse_args()
		keyword = args['keyword']
		page = args['page']
		search_id = args['search_id']
		# TO BE IMPLEMENTED: Randomize the Usage of Cookies
		cookie = cookies[0]

		# Return the first page of search result as requested
		if int(page) == 1 or int(search_id) == -1:
			html_data = plugin_search.retrieve_search_result(SEARCH_URL = SEARCH_URL, keyword = keyword, payload = payload_for_basic_search, cookie = cookie)
			parsed_search_results = plugin_search.parse_html(html_data = html_data, res = res)
			return jsonify(number_of_results = parsed_search_results[0] ,results = parsed_search_results[1], search_id = parsed_search_results[2])

		# Return more pages of search result as requested
		if int(page) > 1 and int(search_id) > 0:
			html_data = plugin_search.retrieve_search_result_in_select_page(SEARCH_RESULT_URL = SEARCH_RESULT_URL, page = page, search_id = search_id, cookie = cookie)
			parsed_search_results = plugin_search.parse_html(html_data = html_data, res = res)
			return jsonify(number_of_results = parsed_search_results[0] ,results = parsed_search_results[1], search_id = parsed_search_results[2])
	
	# For Testing Purposes Only
#	def get(self):
#		keyword = 'wesker'
		# TO BE IMPLEMENTED: Randomize the Usage of Cookies
#		cookie = cookies[0]
#		html_data = plugin_search.retrieve_search_result(SEARCH_URL = SEARCH_URL, keyword = keyword, payload = payload_for_basic_search, cookie = cookie)
#		parsed_search_results = plugin_search.parse_html(html_data = html_data, res = res)
#		return jsonify(number_of_results = parsed_search_results[0] ,results = parsed_search_results[1], search_id = parsed_search_results[2])

	# For Testing Purposes Only
	def get(self):
		page = 2
		search_id = 565
		cookie = cookies[0]

		html_data = plugin_search.retrieve_search_result_in_select_page(SEARCH_RESULT_URL = SEARCH_RESULT_URL, page = page, search_id = search_id, cookie = cookie)
		parsed_search_results = plugin_search.parse_html(html_data = html_data, res = res)
		return jsonify(number_of_results = parsed_search_results[0] ,results = parsed_search_results[1], search_id = parsed_search_results[2])

class SectionInfo(Resource):
	def get(self):
		global section_info
		if len(section_info) == 0 or time.time() - timer_for_refreshing_cached_section_info >= 3600:
			result_tuple = plugin_sectioninfo.retrieve_section_info(related_forum_ids, g, forum_sections)
			# threads, posts, todayposts
			section_info = [result_tuple[0], result_tuple[1], result_tuple[2]]

		return jsonify(threads = section_info[0], posts = section_info[1], todayposts = section_info[2])

class RetrieveThreads(Resource):
	def post(self):
		args = parser_for_retrieving_threads.parse_args()
		fid = args['fid']
		sort_id = args['sort_id']
		limit_multiplier = args['limit_multiplier']
		threads = plugin_retrievethreads.retrieve_threads(fid = fid, sort_id = sort_id, limit_multiplier = limit_multiplier, g = g, forum_threads = forum_threads)
		return jsonify(results = threads)

	# For Testing Purpose Only
	def get(self):
		fid = 50
		limit_multiplier = 1
		start = time.time()
		threads = plugin_retrievethreads.retrieve_threads(fid = fid, sort_id = -1, limit_multiplier = limit_multiplier, g = g, forum_threads = forum_threads)
		length = start - time.time()
		print(length)
		return jsonify(results = threads)

class RetrievePosts(Resource):
	def post(self):
		args = parser_for_retrieving_posts.parse_args()
		tid = args['tid']
		author_id = args['author_id']
		limit_multiplier = args['limit_multiplier']
		posts = plugin_retrieveposts.retrieve_posts(tid = tid, author_id = author_id, limit_multiplier = limit_multiplier, g = g, forum_post = forum_posts)
		return jsonify(results = posts)

	# For Testing Purpose Only
	def get(self):
		tid = 6
		author_id = -1
		limit_multiplier = 1
		posts = plugin_retrieveposts.retrieve_posts(tid = tid, author_id = author_id, limit_multiplier = limit_multiplier, g = g, forum_post = forum_posts)
		return jsonify(results = posts)


api.add_resource(CheckServerStatus, '/serverstatus')
api.add_resource(UserAuthentication, '/userauthentication')
api.add_resource(BasicSearch, '/basicsearch')
api.add_resource(SectionInfo, '/sectioninfo')
api.add_resource(RetrieveThreads, '/retrievethreads')
api.add_resource(RetrievePosts, '/retrieveposts')

if __name__=='__main__':
	app.debug=True
	app.run(host='0.0.0.0', port=8000)