# Imports
from presidency.models import Proclamation, db
from lxml import html
import json
import requests
import datetime

class ProclamationScraper:

	def __init__(self):
		pass

	@staticmethod
	def scrape():

		# Retrieve main Executive Orders page for all potential years.
		page = requests.get('http://www.presidency.ucsb.edu/proclamations.php')
		tree = html.document_fromstring(page.text)

		years = tree.xpath('//select[@id="year"]')[0].xpath('option')
		years = [int(x.text_content()) for x in years][::-1]

		orders = []

		for year in years:
			url = "http://www.presidency.ucsb.edu/proclamations.php?year=%d&Submit=DISPLAY" % year

			page = requests.get(url)
			tree = html.document_fromstring(page.text)

			table = tree.xpath('//form[@name="proclamations"]')[0].getnext().xpath('tr')

			for i in range(1, len(table)):

				data = table[i].xpath('td')

				obj = {
					"president": data[0].text_content(),
					"date": data[1].text_content(),
					"pid": data[2].xpath('a')[0].attrib['href'].split('=')[1],
					"link": "http://www.presidency.ucsb.edu" + data[2].xpath('a')[0].attrib['href'][2:]
				}

				order = 'http://www.presidency.ucsb.edu/ws/index.php?pid=%s' % obj['pid']

				page = requests.get(order)
				tree = html.document_fromstring(page.text)

				obj.update({
					"text" : tree.xpath('//span[@class="displaytext"]')[0].text_content(),
					"date": tree.xpath('//span[@class="docdate"]')[0].text_content(),
					"title": tree.xpath('//title')[0].text_content(),
					"president": tree.xpath('//title')[0].text_content().split(':')[0]
				})

				try:
					order = Proclamation(obj['pid'], obj['title'], obj['text'], obj['link'], datetime.datetime.strptime(obj['date'], "%B %d, %Y"), obj['president'])
					db.session.add(order)
					db.session.commit()
					print("Proclamation retrieved: %s" % obj['pid'])
				except:
					print("Proclamation %s not persisted." % obj['pid'])


			print("Year retrieved: %d" % year)