# Imports
from presidency.models import President, DocumentCategory, Document, db
from lxml import html
import json
import requests
import datetime
from twython import Twython
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Cabinet:

	def __init__(self):
		pass

	@staticmethod
	def scrape():
		pass