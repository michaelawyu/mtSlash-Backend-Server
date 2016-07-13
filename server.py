from flask import Flask, render_template, g, request, redirect, url_for, jsonify
from sqlalchemy import *
from flask_restful import Resource, Api, reqparse
import plugin_userauthentication
import json

app = Flask(__name__)
api = Api(app)

f = open('settings.config','r')
settingsInFile = f.readlines()

settings = {}

for line in settingsInFile:
	items = line.split('=')
	try:
		settings[items[0]] = int(items[1])
	except:
		settings[items[0]] = items[1]

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

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
		args = parser.parse_args()
		username = args['username']
		password = args['password']
		ifAuthenticationPassed = plugin_userauthentication.authenticate(username, password)
		if ifAuthenticationPassed == True:
			return 'OK'
		else:
			return 'FAILED'

api.add_resource(CheckServerStatus, '/serverstatus')
api.add_resource(UserAuthentication, '/userauthentication')

if __name__=='__main__':
	app.debug=True
	app.run(host='0.0.0.0', port=8000)