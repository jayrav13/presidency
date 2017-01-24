# Imports
from presidency.models import *
from lxml import html
import requests
import json
import datetime
from twython import Twython
import os
import time
import sys

# Establish Base URL.
base_url = os.environ.get('WHITE_HOUSE_URL') + "/briefing-room/"

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
	"vetoed-legislation": "Vetoed Legislation"
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
			"document_date": x.xpath('div[contains(@class, "views-field-created")]')[0].text_content().strip() if len(x.xpath('div[contains(@class, "views-field-created")]')) > 0 else x.xpath('div')[0].text_content().split(' on ')[1],
			"title": x.xpath('div[contains(@class, "views-field-title")]')[0].text_content().strip(),
			"uri": x.xpath('div[contains(@class, "views-field-title")]')[0].xpath('h3')[0].xpath('a')[0].attrib['href'].strip(),
			"category_slug": key,
			"category_name": value
		} for x in tree.xpath('//div[contains(@class, "views-row")]')]

		records = [WhiteHouse(x['title'], x['uri'], x['category_slug'], x['category_name'], x['document_date']) for x in objects]
		count = 0
		for x in records:
			try:
				db.session.add(x)
				db.session.commit()
				print("Added " + x.title + " successfully.")
				count += 1
			except Exception as e:
				db.session.rollback()
				print("Failed to add " + x.title + " successfully: " + str(e))

		# If 0 records were added to the database, everything henceforth is old in this topic.
		# Break, go to next slug.
		if count == 0:
			break

# Check if this environment should tweet. If not, exit.
if not os.environ.get('TWEET_ENV') == 'TRUE':
	sys.exit()

# Retrieve all documents in descending order.
documents = WhiteHouse.query.filter_by(is_tweeted=False).order_by(WhiteHouse.id.asc())

# Set up Twitter bot.
twitter = Twython(
	os.environ.get('TWITTER_CONSUMER_KEY'),
	os.environ.get('TWITTER_CONSUMER_SECRET'),
	os.environ.get('TWITTER_ACCESS_TOKEN'),
	os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
)

for document in documents:
	
	url = requests.post('https://www.googleapis.com/urlshortener/v1/url?key=' + os.environ.get('GOOGLE_URL_SHORTENER_API_KEY'), json={"longUrl": os.environ.get('WHITE_HOUSE_URL') + document.uri})
	if url.status_code == 200:
		url = url.json()['id']
	else:
		url = os.environ.get('WHITE_HOUSE_URL') + document.uri

	"""
	https://support.twitter.com/articles/78124

	All links are resized to 23 characters. Account for this.
	"""
	if(len(document.title) < 116): # Taking out the length of URL + 1 space for a space between the two, does this fit?
		twitter.update_status(status=(document.title + " " + url))
	else: # Truncate title and add ellipse.
		print(document.title[0:113] + "... " + url)
		twitter.update_status(status=(document.title[0: 113] + "... " + url))

	print("Tweeted: " + document.title + " - " + str(document.id))

	document.is_tweeted = True

	try:
		db.session.add(document)
		db.session.commit()
		print("Updated object saved successfully (id: " + str(document.id) + ")")
	except Exception as e:
		db.session.rollback()
		print("Could not save updated object (id: " + str(document.id) + " - " + str(e))

	print("Sleeping...")
	time.sleep(10)