# Establish imports.
from flask import Blueprint, request, jsonify, url_for, render_template, make_response, abort, current_app
from flask_json import json_response, as_json
from presidency import app, db, auth
from .models import *
from datetime import datetime
from requests.auth import HTTPBasicAuth
from functools import wraps
from lib.appointments import Appointments
import os
import requests
import json

from urlparse import urljoin
from flask import request
from werkzeug.contrib.atom import AtomFeed


def make_external(url):
	return urljoin(request.url_root, url)

"""
/rss

RSS Feed
"""
@app.route('/rss')
def rss_feed():

	feed = AtomFeed('White House Briefing Room Releases', feed_url=request.url, url=request.url_root)

	documents = WhiteHouse.query.order_by(WhiteHouse.document_date.desc())

	for document in documents:

		feed.add(document.title, document.tweet,
			content_type='text',
			author="@presproject2017",
			url=make_external(document.full_url),
			updated=document.document_date,
			published=document.document_date)

	return feed.get_response()

@app.route('/appointments')
def appointments_ui():

	# Appointments
	appointments = Appointments()
	data = appointments.scrape()

	counts = {
		"total": 0,
		"confirmation": {
			"required": {
				"total": 0,
				"appointed": 0,
				"confirmed": 0
			},
			"not_required": {
				"total": 0,
				"confirmed": 0
			}
		},
		"secretary": {
			"total": 0,
			"appointed": 0,
			"confirmed": 0
		},
		"deputy_secretary": {
			"total": 0,
			"appointed": 0,
			"confirmed": 0
		}
	}

	# Iterate through all departments for which political appointments are made.
	for department in data['political']:

		# Iterate through appointees of each department.
		for appointee in department['appointees']:

			# Count total number of appointees.
			counts['total'] += 1

			# Split into required vs non required confirmation
			if appointee['details']['senate']['is_confirmation_required']:
				counts['confirmation']['required']['total'] += 1
				if appointee['appointee'] is not None:
					counts['confirmation']['required']['appointed'] += 1
				if appointee['details']['senate']['is_confirmed']:
					counts['confirmation']['required']['confirmed'] += 1

				if appointee['details']['position']['is_secretary']:
					counts['secretary']['total'] += 1
					if appointee['appointee'] is not None:
						counts['secretary']['appointed'] += 1
					if appointee['details']['senate']['is_confirmed']:
						counts['secretary']['confirmed'] += 1

				if appointee['details']['position']['is_deputy_secretary']:
					counts['deputy_secretary']['total'] += 1
					if appointee['appointee'] is not None:
						counts['deputy_secretary']['appointed'] += 1
					if appointee['details']['senate']['is_confirmed']:
						counts['deputy_secretary']['confirmed'] += 1

			else:
				counts['confirmation']['not_required']['total'] += 1
				if appointee['appointee'] is not None:
					counts['confirmation']['not_required']['confirmed'] += 1
			

	print counts

	return render_template('appointments.html', 
		appointments=appointments,
		counts=counts
	)

"""
/api/v1/heartbeat

Return HTTP 200 if the server is up and running.
"""
@app.route('/api/v1/heartbeat')
def heartbeat():
	return make_response(jsonify({"success": True}), 200)

@app.route('/api/v1/documents')
def documents():

	docs = WhiteHouse.query.order_by(WhiteHouse.document_date.desc()).order_by(WhiteHouse.title.asc())
	docs = [doc.to_json() for doc in docs]
	return make_response(jsonify({"documents": docs}), 200)

@app.route('/api/v1/appointments')
def appointments():

	appointments = Appointments()
	return make_response(jsonify(appointments.scrape()), 200)
