#-*-coding:utf-8-*-

from flask import Blueprint

api = Blueprint('api', __name__)
from api import user
from api import activity
from api import blog
from api import message
from api import news