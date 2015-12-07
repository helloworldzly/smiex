#-*-coding:utf-8-*-

import requests

def add_activity():
	url = "http://127.0.0.1:5000/api/activity/admin/add"
	para = {
		'title':'hahaha',
		'description':'hehehe',
		'startyear':'2014',
		'startmonth':'11',
		'startday':'30',
		'starthour':'5',
		'startminute':'30',
		'endyear':'2015',
		'endmonth':'11',
		'endday':'30',
		'endhour':'6',
		'endminute':'7',
		'attendtype':'0',
		'peoplenum':'30',
		'filter':'0',
		'bstartyear':'2015',
		'bstartmonth':'12',
		'bstartday':'01',
		'bstarthour':'5',
		'bstartminute':'30',
		'bendyear':'2016',
		'bendmonth':'11',
		'bendday':'30',
		'bendhour':'6',
		'bendminute':'7',
		'fuzeren':'zzy',
		'fuzerenphone':'110',
		'poster':'0',
		'appendproblem':'0'
	}

	res = requests.post(url, data=para)
	print res.text

def edit_activity():
	url = "http://127.0.0.1:5000/api/activity/admin/edit"
	para = {
		'activityid':'10003',
		'bstartyear':'2014',
		'bstartmonth':'11',
		'bstartday':'30',
		'bstarthour':'5',
		'bstartminute':'30',
		'bendyear':'2016',
		'bendmonth':'11',
		'bendday':'30',
		'bendhour':'6',
		'bendminute':'7',
	}

	res = requests.post(url, data=para)
	print res.text

def activity_info():
	url = "http://127.0.0.1:5000/api/activity/info/10009"
	res = requests.get(url)
	print res.text

def activity_member():
	url = "http://127.0.0.1:5000/api/activity/member/10002"
	res = requests.get(url)
	print res.text

def activity_sign_up():
	url = "http://127.0.0.1:5000/api/activity/signup/person/10009"
	res = requests.post(url)
	print res.text

def activity_sign_down():
	url = "http://127.0.0.1:5000/api/activity/signdown/person/10009"
	res = requests.post(url)
	print res.text

def get_file_list():
	url = "http://127.0.0.1:5000/api/files/catalog/bii"
	res = requests.get(url)
	print res.text

if __name__ == '__main__':
	#add_activity()
	#activity_info()
	#activity_member()
	#edit_activity()
	#activity_sign_up()
	#activity_info()
	#activity_sign_down()
	#activity_info()
	get_file_list()