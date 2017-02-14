# Establish imports.
from flask import Blueprint, request, jsonify, url_for, render_template, make_response, abort, current_app
from flask_json import json_response, as_json
from presidency import app, db, auth
from .models import *
from datetime import datetime
from requests.auth import HTTPBasicAuth
from functools import wraps
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