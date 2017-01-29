from presidency import app, db
import datetime

class WhiteHouse(db.Model):
	"""
	WhiteHouse

	All Briefing Room releases by the White House.
	"""

	__tablename__ = 'wh_documents'

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	title = db.Column(db.Text)
	uri = db.Column(db.Text, unique=True)
	is_tweeted = db.Column(db.Boolean, default=False)
	category_slug = db.Column(db.String(255), nullable=True)
	category_name = db.Column(db.String(255), nullable=True)
	document_date = db.Column(db.DateTime, nullable=True)

	full_url = db.Column(db.String, nullable=True)
	short_url = db.Column(db.String, nullable=True)

	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

	def __init__(self, title, uri, category_slug=None, category_name=None, document_date=None, full_url=None, short_url=None):
		self.title = title
		self.uri = uri
		self.category_slug = category_slug
		self.category_name = category_name
		self.document_date = datetime.datetime.strptime(document_date, "%B %d, %Y") if document_date != None else document_date
		self.full_url = full_url
		self.short_url = short_url


class Error(db.Model):
	"""
	Error

	Store exceptions for future review.
	"""

	__tablename__ = 'errors'

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	error_message = db.Column(db.Text, nullable=True)

	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

	def __init__(self, error_message):
		self.error_message = error_message