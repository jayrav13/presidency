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

class Scraper:

	def __init__(self):
		pass

	@staticmethod
	def scrape(full_scrape=False):
		"""
		scrape()
		Scrape data.
		"""

		# Retrieve home page on which all data lives.
		page = requests.get('http://www.presidency.ucsb.edu')
		tree = html.document_fromstring(page.text)

		"""
		Presidents

		Retrieve all US Presidents.
		"""
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


		"""
		Categories

		Retrieve all possible Document Categories.
		"""
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

		"""
		Documents

		Retrieve all Documents.
		"""

		# Check if we're scraping all presidents.
		presidents = None

		if full_scrape:
			presidents = President.query.all()
		else:
			presidents = [ President.query.order_by(President.number.desc()).first() ]

		categories = DocumentCategory.query.all()

		# Iterate through m Presidents * n Categories.
		for president in presidents:
			for category in categories:

				response = requests.post('http://www.presidency.ucsb.edu/ws/index.php', data={
					"pres": president.number,
					"ty": category.number
				})

				tree = html.document_fromstring(response.text)
				rows = []
				try:
					rows = tree.xpath('//td[@class="listname"]')[0].getparent().getparent().xpath('tr')
				except:
					pass

				for row in rows:
					data = row.xpath('td')
					if len(data) == 4 and 'class' in data[0].attrib and data[0].attrib['class'] == 'listdate':

						try:
							document = Document(int(data[3].xpath('font')[0].xpath('a')[0].attrib['href'].split('?', 1)[1].split('&', 1)[0].split('=', 1)[1]), datetime.datetime.strptime(data[0].text_content().strip(), "%B %d, %Y"), data[3].text_content().strip())
							document.president_id = president.id
							document.document_category_id = category.id
							db.session.add(document)
							db.session.commit()

							print(president.name + " - " + category.type + " - " + document.title)
						except Exception as e:
							print(str(e))
							db.session.rollback()
					else:
						pass

	@staticmethod
	def build():
		"""
		Queries, set up variables.
		"""
		presidents = President.query.filter(President.number <= 44)
		categories = DocumentCategory.query.all()

		data = {}
		sum = 0

		"""
		Iterate through every president / category combination and add data.
		"""
		for president in presidents:

			data[president.name] = {}

			for category in categories:

				# Add key if needed.
				if category.type not in data[president.name]:
					data[president.name][category.type] = []

				# Retrieve relevant documents and extend the current array with all documents found in this category.
				documents = Document.query.filter_by(president_id=president.id).filter_by(document_category_id=category.id).all()

				data[president.name][category.type].extend([{
					"pid": document.pid,
					"document_date": str(document.document_date),
					"title": document.title,
					"category": category.category,
					"subcategory": category.subcategory
				} for document in documents])

		return data
