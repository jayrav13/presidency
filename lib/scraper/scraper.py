# Imports
from presidency.models import President, DocumentCategory, db
from lxml import html
import json
import requests
import datetime

class Scraper:

	def __init__(self):
		pass

	@staticmethod
	def scrape():
		"""
		scrape()
		Scrape data.
		"""


		# Retrieve home page on which all data lives.
		page = requests.get('http://www.presidency.ucsb.edu')
		tree = html.document_fromstring(page.text)

		# Scrape and store Presidents.
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
				db.session.rollback()

		# Scrape and store Document Categories.
		categories = tree.xpath('//select[@id="select12"]')[0].xpath('option')
		categories = [{
			"full_text": x.text_content(),
			"number": int(x.attrib['value']),
			"type": x.text_content().split(':')[0],
			"category": x.text_content().split(':')[1].split('-', 1)[0].strip() if len(x.text_content().split(':')) > 1 else None,
			"subcategory": x.text_content().split('-', 1)[1].strip() if len(x.text_content().split('-', 1)) > 1 else None
		} for x in categories if x.text_content() != 'Document Category']

		for category in categories:
			try:
				category = DocumentCategory(category['full_text'], category['number'], category['type'], category['category'], category['subcategory'])
				db.session.add(category)
				db.session.commit()
			except:
				db.session.rollback()

