# Imports
from presidency.models import President, db
from lxml import html
import json
import requests
import datetime

class PresidentScraper:

	def __init__(self):
		pass

	@staticmethod
	def scrape():
		"""
		scrape()

		Retrieve and store all Presidents.
		"""
		page = requests.get('http://www.presidency.ucsb.edu')
		tree = html.document_fromstring(page.text)

		presidents = tree.xpath('//select[@id="select10"]')[0].xpath('option')
		presidents = [{
			"name": x.text_content(),
			"number": int(x.attrib['value'])
		} for x in presidents if x.text_content() != 'President']

		for president in presidents:
			try:
				president = President(president['name'], president['number'])
				db.session.add(president)
				db.session.commit()
			except:
				pass