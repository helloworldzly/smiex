#-*-coding:utf-8-*-

from server import app
from flask import render_template, make_response, request, redirect

@app.route('/login', methods=['GET'])
def login():
	cookies = request.cookies
	if 'session' in cookies:
		session = cookies['session']
		from lib import get_username_by_session
		username = get_username_by_session(session)
		if username != None:
			return redirect('/')
	else:
		from lib import generate_session
		session = generate_session()

	resp = make_response(render_template('login.html'))
	resp.set_cookie('session', session, max_age=120)
	return resp

@app.route('/', methods=['GET'])
def index():
	cookies = request.cookies
	if 'session' in cookies:
		session = cookies['session']
		from lib import get_username_by_session
		username = get_username_by_session(session)
		if username == None:
			# resp = make_response(redirect('/'))
			resp = make_response(render_template("index.html"))
			resp.delete_cookie('session')
			return resp
		else:
			resp = make_response(render_template("index.html", username=username, islogin=1))
			resp.set_cookie('session', session, max_age=120)
			return resp
	else:
		return render_template("index.html")

@app.route('/dashboard', methods=['GET'])
def add():
	return render_template("dashboard.html")

@app.route('/test', methods=['GET'])
def test():
	return render_template("test.html")

@app.route('/activity/<activityid>', methods=['GET'])
def activity(activityid):
	return render_template("activity.html", activityid=activityid)

@app.route('/activitylist', methods=['GET'])
def activitylist():
	return render_template("activitylist.html")

@app.route('/download/<regex(".*"):path>', methods=['GET'])
def download(path):
	return render_template("download.html",path=path)