# Imports
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

		# Return Wikipedia page and turn into a tree.
		base_url = 'https://en.wikipedia.org'
		response = requests.get(base_url + '/wiki/Cabinet_of_the_United_States')
		tree = html.document_fromstring(response.text)

		# Get all of the rows of the Cabinet table.
		rows = tree.xpath('//th[text()="Cabinet"]')[0].getparent().getparent().getchildren()
		
		obj = []

		# Iterate through all rows.
		for x in rows:

			# Retrieve all of the elements per row.
			data = x.getchildren()

			# Only look at this if we're looking at Cabinet members.
			if len(data) == 3 and data[0].tag == 'td':

				# Clean up data with strip.
				obj.append({
					"title": [x for x in data[0].text_content().split('\n') if x != ''][0],
					"seal": 'https:' + data[0].xpath('a/img')[0].attrib['src'],
					"img": 'https:' + data[1].xpath('a/img')[0].attrib['src'],
					"name": [x for x in data[1].text_content().split('\n') if x != ''][0],
					"details": base_url + data[1].xpath('div/a')[0].attrib['href'],
					"is_acting": (len([x for x in data[1].text_content().split('\n') if x != '']) > 1 and [x for x in data[1].text_content().split('\n') if x != ''][1] == 'Acting'),
					"date_appointed": data[2].text_content(),
				})

		print(json.dumps(obj))