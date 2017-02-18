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
Appointments

Retrieve all presidential appointments.
"""
class Appointments:

	def __init__(self):
		self._base_url = 'https://en.wikipedia.org'
		self._response = requests.get(self._base_url + '/wiki/Political_appointments_of_Donald_Trump')
		self._tree = html.document_fromstring(self._response.text)

	def scrape(self):
		"""
		scrape()

		Public function that returns JSON data.
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
						"data": organization
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

				organization.append(appointee)

		return {"political": output}

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