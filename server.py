from flask import Flask, render_template, g, request, redirect, url_for, jsonify
from sqlalchemy import *
from flask_restful import Resource, Api, reqparse
from bs4 import BeautifulSoup
import plugin_userauthentication
import plugin_search
import init_cookies
import json
import requests

app = Flask(__name__)
api = Api(app)

# Set Constants (Search URL)
SEARCH_URL = 'http://mtslash.org/search.php'

# Set Constants (Payload for Basic Search)
payload_for_basic_search = {}
payload_for_basic_search['formhash'] = 'b6ba6cb8'
payload_for_basic_search['searchsubmit'] = 'yes'
payload_for_basic_search['srchtxt'] = ''

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

# Initialize a Parser For User Authentication 
parser_for_userauthentication = reqparse.RequestParser()
parser_for_userauthentication.add_argument('username')
parser_for_userauthentication.add_argument('password')

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
def privacypolicy():
	return render_template('whatsnew.html')

@app.route('/userexpimprovproj')
def privacypolicy():
	return render_template('userexpimprovproj.html')

class CheckServerStatus(Resource):
	def get(self):
		return jsonify(**settings)

class UserAuthentication(Resource):
	def post(self):
		args = parser_for_userauthentication.parse_args()
		username = args['username']
		password = args['password']
		ifAuthenticationPassed = plugin_userauthentication.authenticate(username, password)
		if ifAuthenticationPassed == True:
			return 'OK'
		else:
			return 'FAILED'

class BasicSearch(Resource):
	def post(self):
		raise NotImplementedError

api.add_resource(CheckServerStatus, '/serverstatus')
api.add_resource(UserAuthentication, '/userauthentication')
api.add_resource(BasicSearch, '/basicsearch')

if __name__=='__main__':
	app.debug=True
	app.run(host='0.0.0.0', port=8000)