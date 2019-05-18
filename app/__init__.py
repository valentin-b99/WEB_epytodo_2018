##
## EPITECH PROJECT, 2018
## __init__.py
## File description:
## __init__
##

import os
import locale
from app.controllers import *
from flask import *
import pymysql as sql

app = Flask(__name__)
#app.secret_key = os.urandom(42)
app.secret_key = 'WJ35b78rPjr8WAiu7aq9CVb1337mtJ4d7M5t9uP59N'
app.config.from_object('config')
locale.setlocale(locale.LC_TIME, "")

def get_application():
    return app

conn = ConnectionManager(app)

def get_connection():
    return conn.get_connection()

@app.template_filter('autoversion')
def autoversion_filter(filename):
  fullpath = os.path.join('app/', filename[1:])
  try:
      timestamp = str(os.path.getmtime(fullpath))
  except OSError:
      return filename
  newfilename = "{0}?v={1}".format(filename, timestamp)
  return newfilename
