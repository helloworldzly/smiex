#-*-coding:utf-8-*-

from flask import Flask
from werkzeug.routing import BaseConverter
from api import api

class Converter(BaseConverter):
	def __init__(self, map, *args):
		self.map=map
		self.regex = args[0]

app = Flask(__name__, template_folder='web/templates')
app.url_map.converters['regex'] = Converter

app.debug = True
app.register_blueprint(api, url_prefix='/api')

from web import *

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)