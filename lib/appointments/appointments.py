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


from lib.senators import Senators
"""
Appointments

Retrieve all presidential appointments.
"""
class Appointments:

	def __init__(self):
		self._base_url = 'https://en.wikipedia.org'
		self._response = requests.get(self._base_url + '/wiki/Political_appointments_of_Donald_Trump')
		self._tree = html.document_fromstring(self._response.text)

		self._congress_url = '/wiki/List_of_United_States_Senators_in_the_115th_Congress_by_seniority'
		self._senators_scraper = Senators(self._congress_url)
		self._senators = self._senators_scraper.scrape()

	def scrape(self):
		return {'political': self._political()}

	def _political(self):
		"""
		_political()

		Public function that returns JSON data for political appointments.
		"""

		# Get the editable table 
		headers = self._tree.xpath('//table[contains(@class, "wikitable")]')[0]

		# Prepare arrays to store all of this data.
		output = []
		organization = []

		# Iterate through all rows
		for row in headers.xpath('tr'):

			# Return data per row.
			data = row.xpath('td')

			# Check if this row contains the name of a government agency.
			hl = self._extract_agency(row)
			if hl is not None:

				# If we've hit a gov't agency header and data for it exists.
				if len(organization) > 0:

					# Create a data structure, add org data and append to final output.
					# Reset organization array.
					build = {
						"name": headline,
						"appointees": organization
					}
					output.append(build)
					organization = []

				# Set new organization headline.
				headline = hl

			# If this row has appointee data.
			if len(data) > 0:

				appointee = {}
				appointee['position'] = data[0].text_content().strip('\n')
				appointee['appointee'] = None if len(data[1].text_content().strip('\n')) == 0 else data[1].text_content().strip('\n')

				appointee['assets'] = {}
				appointee['assets']['seal'] = self._extract_image(data[0])
				appointee['assets']['img'] = self._extract_image(data[1])

				appointee['details'] = {}
				appointee['details']['senate'] = {}
				appointee['details']['senate']['is_confirmation_required'] = '(without Senate confirmation)' not in data[2].text_content()
				appointee['details']['senate']['is_confirmed'] = 'Confirmed by Senate' in data[2].text_content() if appointee['details']['senate']['is_confirmation_required'] else None

				breakdown = data[2].text_content().split('\n')
				print breakdown
				if appointee['details']['senate']['is_confirmed']:

					appointee['details']['senate']['vote'] = {}
					if len(breakdown) >= 2:
						vote = self._extract_vote(breakdown[1])

						if vote is not None and len(vote) == 2:
							appointee['details']['senate']['vote']['aye'] = vote[0]
							appointee['details']['senate']['vote']['nay'] = vote[1]
							appointee['details']['senate']['vote']['dissent'] = []

							if len(breakdown) >= 3:
								appointee['details']['senate']['vote']['dissent'] = self._extract_dissent(breakdown[2], data[2])

				organization.append(appointee)

		return output

	def _extract_image(self, element):
		"""
		_extract_image()

		Attempt to find an image and return.
		"""
		a = element.xpath('a')
		if len(a) == 0:
			return None

		img = a[0].xpath('img')
		if len(img) == 0:
			return None

		return "https:" + img[0].attrib['src']

	def _extract_agency(self, element):
		"""
		_extract_agency()

		Attempt to return an agency header.
		"""
		th = element.xpath('th')
		if len(th) == 0:
			return None

		h3 = th[0].xpath('h3')
		if len(h3) == 0:
			return None

		headline = h3[0].xpath('span[@class="mw-headline"]')
		if len(headline) == 0:
			return None

		return headline[0].text_content()

	def _extract_vote(self, string):
		"""
		_extract_vote()

		Given a string, extract the vote count from it.
		"""

		# Make sure that this person was confirmed by the Senate. Should be.
		if 'Confirmed by Senate' not in string:
			return None

		# Split the string by the first parenthasis at beginning of vote count.
		split = string.split('(')

		if len(split) != 2:
			return None

		# Swap out second parenthasis and then try to split.
		vote = split[1].replace(')', '').split('-')

		# Handle UTF-8 dash.
		if len(vote) == 1:
			vote = vote[0].encode('utf-8').split('\xe2\x80\x93')

		# Final check.
		if len(vote) != 2:
			# Something went wrong.
			return None

		# Return vote count.
		try:
			vote = [int(x.replace('*', '')) for x in vote]
			return vote
		except:
			return None

	def _extract_dissent(self, string, element):

		common_phrase = 'Dissenting votes:'

		if common_phrase not in string:
			return None

		small = element.xpath('small')
		if len(small) != 1:
			return None

		a = small[0].xpath('a')

		senators = []

		for senator in a:
			if 'href' in senator.attrib and senator.attrib['href'] in self._senators:
				senators.append(self._senators[senator.attrib['href']])
			else:
				senators.append({"name": senator.text_content() })
		return senators
