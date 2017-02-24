"""
Imports
"""
from presidency.models import *
from lxml import html
import requests
import json
import datetime
from twython import Twython
import os
import time
import sys

"""
Set UTF-8 for everything.
"""
reload(sys)
sys.setdefaultencoding("utf-8")

# Establish Base URL.
base_url = os.environ.get('WHITE_HOUSE_URL') + ""

# Establish all pages to scrape.
pages = {
	"/briefing-room/speeches-and-remarks": "Speeches and Remarks",
	"/briefing-room/press-briefings": "Press Briefings",
	"/briefing-room/statements-and-releases": "Statements and Releases",
	"/briefing-room/presidential-actions/executive-orders": "Executive Orders",
	"/briefing-room/presidential-actions/presidential-memoranda": "Presidential Memoranda",
	"/briefing-room/presidential-actions/proclamations": "Proclamations",
	"/briefing-room/presidential-actions/related-omb-material": "Related OMB Material",
	# "/briefing-room/pending-legislation": "Pending Legislation",
	# "/briefing-room/signed-legislation": "Signed Legislation",
	# "/briefing-room/vetoed-legislation": "Vetoed Legislation",
	"/briefing-room/statements-administration-policy": "Statements of Administration Policy"
}

# Scrape each page.
for key, value in pages.iteritems():
	
	print("Scanning " + value)

	# Make request and transform into tree.
	page_url = base_url + key
	response = requests.get(page_url)
	tree = html.document_fromstring(response.text)

	# Deterimine number of total pages.
	pagecount = int(tree.xpath('//li[@class="pager-current"]')[0].text_content().split(' of ')[1]) if len(tree.xpath('//li[@class="pager-current"]')) > 0 else 1

	# Keep iterating through pages until you reach a page that has been fully scraped. Then stop.
	for i in range(0, pagecount):

		# Use ?page= parameter to scrape, starting with page 0.
		response = requests.get(page_url)
		print("PAGE URL: " + page_url)
		tree = html.document_fromstring(response.text)

		# Build the resulting dictionary objects for each document on that page.
		objects = [{
			"document_date": x.xpath('div[contains(@class, "views-field-created")]')[0].text_content().strip() if len(x.xpath('div[contains(@class, "views-field-created")]')) > 0 else x.xpath('div')[0].text_content().split(' on ')[1],
			"title": x.xpath('div[contains(@class, "views-field-title")]')[0].text_content().strip(),
			"uri": x.xpath('div[contains(@class, "views-field-title")]')[0].xpath('h3')[0].xpath('a')[0].attrib['href'].strip(),
			"category_slug": key,
			"category_name": value,
			"full_url": os.environ.get('WHITE_HOUSE_URL') + x.xpath('div[contains(@class, "views-field-title")]')[0].xpath('h3')[0].xpath('a')[0].attrib['href'].strip()
		} for x in tree.xpath('//div[contains(@class, "views-row")]')]

		# Add url's to object.
		for i in range(0, len(objects)):

			url = requests.post('https://www.googleapis.com/urlshortener/v1/url?key=' + os.environ.get('GOOGLE_URL_SHORTENER_API_KEY'), json={"longUrl": os.environ.get('WHITE_HOUSE_URL') + objects[i]['uri']})

			if url.status_code == 200:
				objects[i]['short_url'] = url.json()['id']
			else:
				objects[i]['short_url'] = objects[i]['short_url']

		# Create database objects for all of these.
		records = [WhiteHouse(x['title'], x['uri'], x['category_slug'], x['category_name'], x['document_date'], x['full_url'], x['short_url']) for x in objects]

		# Track number of records successfully added. Those not added will be duplicates.
		record_counter = 0

		# Iterate through records.
		for x in records:

			# Attempt to persist.
			try:

				db.session.add(x)
				db.session.commit()

				record_counter = record_counter + 1
				
				print("Added " + x.title + " successfully.")

			# Fallback,
			except Exception as e:

				# Flush old commit that did not persist.
				db.session.rollback()

				# Try to save an error message.
				"""
				try:
					db.session.add(Error(str(e)))
					db.session.commit()
				except:
					db.session.rollback()
				"""

				print("Failed to add " + x.title + " successfully: " + str(e))

		# If 0 records were added to the database, everything henceforth is old in this topic.
		# Break, go to next slug.

		pager = tree.xpath('//li[contains(@class, "pager-next")]')
		try:
			print(pager[0].xpath('a')[0].attrib['href'])
			page_url = base_url + pager[0].xpath('a')[0].attrib['href']
		except:
			pass


# Retrieve all documents in descending order.
documents = WhiteHouse.query.filter_by(is_tweeted=False).order_by(WhiteHouse.document_date.asc())

print("New documents detected: %d" % (documents.count()))

# Set up Twitter bot.
twitter = Twython(
	os.environ.get('TWITTER_CONSUMER_KEY'),
	os.environ.get('TWITTER_CONSUMER_SECRET'),
	os.environ.get('TWITTER_ACCESS_TOKEN'),
	os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
)

# Go through all relevant documents and tweet them out.
for document in documents:

	try:
		tweet = document.title[0 : 113] + ("..." if len(document.title) > 113 else "") + " " + document.short_url

		if os.environ.get('TWEET_ENV') == "TRUE":

			try:
				twitter.update_status( status=(tweet) )
				document.is_tweeted = True
			except Exception as e:
				"""
				db.session.add(Error(str(e)))
				db.session.commit()
				"""
				continue

		document.tweet = tweet

		print("Tweeted: " + document.tweet)

		db.session.add(document)
		db.session.commit()

	except Exception as e:
		"""
		try:
			db.session.add(Error(str(e)))
			db.session.commit()
		except:
			db.session.rollback()
		"""
		pass

	# Time Delay
	if os.environ.get('TWEET_ENV') == "TRUE":
		time.sleep(10)


