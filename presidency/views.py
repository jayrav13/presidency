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

"""
/api/v1/heartbeat

Return HTTP 200 if the server is up and running.
"""
@app.route('/api/v1/heartbeat')
def heartbeat():
	return make_response(jsonify({"success": True}), 200)
