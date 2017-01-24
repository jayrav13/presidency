# Imports
from presidency.models import *
from lxml import html
import requests
import json
import datetime
from twython import Twython
import os
import time

# Establish Base URL.
base_url = "https://whitehouse.gov/briefing-room/"

# Establish all potential pages.
pages = {
	"speeches-and-remarks": "Speeches and Remarks",
	"press-briefings": "Press Briefings",
	"statements-and-releases": "Statements and Releases",
	"presidential-actions/executive-orders": "Executive Orders",
	"presidential-actions/presidential-memoranda": "Presidential Memoranda",
	"presidential-actions/proclamations": "Proclamations",
	"pending-legislation": "Pending Legislation",
	"signed-legislation": "Signed Legislation",
	"vetoed-legislation": "Vetoed Legislation",
	"nominations-and-appointments": "Nominations and Appointments"
}

# Iterate through all pages:
for key, value in pages.iteritems():
	
	print("Scanning " + value)

	# Make request and transform into tree.
	response = requests.get(base_url + key)
	tree = html.document_fromstring(response.text)

	# Deterimine number of total pages.
	pagecount = int(tree.xpath('//li[@class="pager-current"]')[0].text_content().split(' of ')[1]) if len(tree.xpath('//li[@class="pager-current"]')) > 0 else 1

	for i in range(0, pagecount):

		# Start pulling pages from the top, this time with the page variable.
		response = requests.get(base_url + key + "?page=" + str(i))
		tree = html.document_fromstring(response.text)
		# print(tree.xpath('//div[contains(@class, "views-row")]'))

		objects = [{
			# TODO:
			# "document_date": x.xpath('div[contains(@class, "views-field-created")]')[0].text_content().strip() if len(x.xpath('div[contains(@class, "views-field-created")]')) > 0 else x.xpath('div[contains(@class, "views-field-field-signed-date")]')[0].xpath('div')[0].xpath('span')[0].text_content(),
			"title": x.xpath('div[contains(@class, "views-field-title")]')[0].text_content().strip(),
			"uri": x.xpath('div[contains(@class, "views-field-title")]')[0].xpath('h3')[0].xpath('a')[0].attrib['href'].strip(),
			"category_slug": key,
			"category_name": value
		} for x in tree.xpath('//div[contains(@class, "views-row")]')]

		records = [WhiteHouse(x['title'], x['uri'], x['category_slug'], x['category_name']) for x in objects]
		for x in records:
			try:
				db.session.add(x)
				db.session.commit()
				print("Added " + x.title + " successfully.")
			except Exception as e:
				db.session.rollback()
				print("Failed to add " + x.title + " successfully: " + str(e))

# Retrieve all documents in descending order.
documents = WhiteHouse.query.filter_by(is_tweeted=False).order_by(WhiteHouse.id.desc())

# Set up Twitter bot.
twitter = Twython(
	os.environ.get('TWITTER_CONSUMER_KEY'),
	os.environ.get('TWITTER_CONSUMER_SECRET'),
	os.environ.get('TWITTER_ACCESS_TOKEN'),
	os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
)

for document in documents:
	try:
		twitter.update_status(status=((document.title if len(document.title) < 120 else document.title[0:119]) + " https://www.whitehouse.gov" + document.uri))
		document.is_tweeted = True
		print("Tweeted: " + document.title + " - " + str(document.id))
	except:
		try:
			twitter.update_status(status=("https://www.whitehouse.gov" + document.uri))
			document.is_tweeted = True
			print("Tweeted LINK ONLY: " + document.title + " - " + str(document.id))
		except:
			document.is_tweeted = False
			print("Could not be tweeted: " + str(document.id))

	try:
		db.session.add(document)
		db.session.commit()
		print("Updated object saved successfully (id: " + str(document.id) + ")")
	except Exception as e:
		db.session.rollback()
		print("Could not save updated object (id: " + str(document.id) + " - " + str(e))

	print("Sleeping...")
	time.sleep(10)