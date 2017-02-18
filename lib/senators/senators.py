# Imports
from lxml import html
import json
import requests
import datetime
from twython import Twython
import os
import sys
import re
reload(sys)
sys.setdefaultencoding("utf-8")

"""
Senators

Return all US Senators.
"""
class Senators:

	def __init__(self, url):
		self._base_url = 'https://en.wikipedia.org'
		self._response = requests.get(self._base_url + url)
		self._tree = html.document_fromstring(self._response.text)

	def scrape(self):
		"""
		scrape()

		Returns a dict of all US senators.
		"""

		# Confirm retrieval of table.
		table = self._tree.xpath('//table[contains(@class, "wikitable")]')
		if len(table) == 0:
			return None
		table = table[0]

		# Set up dict for Senators. Iterate through rows.
		senators = {}

		for row in table.xpath('tr'):

			# Get all data points, ignore any invalid rows (header).
			data = row.xpath('td')
			if len(data) == 0:
				continue

			# Retrieve the unique identifier by Senator, the URL.
			url = data[0].xpath('a')[0].attrib['href'].replace(',', '')

			# Simplify with text only content.
			simple = [x.text_content() for x in data]

			# Add Senator to dict.
			senators[url] = {
				"name": simple[0],
				"party": simple[1],
				"state": simple[2],
				"url": url,
			}

		return senators