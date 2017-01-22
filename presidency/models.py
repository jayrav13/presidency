from presidency import app, db
import datetime

class ExecutiveOrder(db.Model):
	"""
	ExecutiveOrder

	All Executive Orders issued by Presidents of the United States.
	"""

	__tablename__ = 'executive_orders'

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	pid = db.Column(db.Integer, nullable=False)
	title = db.Column(db.Text)
	text = db.Column(db.Text)
	link = db.Column(db.String(255))
	document_date = db.Column(db.DateTime)
	president = db.Column(db.String(255))

	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

	def __init__(self, pid, title = None, text = None, link = None, document_date = None, president = None):
		self.pid = pid
		self.title = title
		self.text = text
		self.link = link
		self.document_date = document_date
		self.president = president

	def to_json(self):
		output = self.__dict__
		for key in output:
			if isinstance(output[key], datetime.datetime):
				output[key] = str(output[key])
		output.pop('_sa_instance_state')

		return output

class Proclamation(db.Model):
	"""

	"""

	__tablename__ = 'proclamations'

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	pid = db.Column(db.Integer, nullable=False)
	title = db.Column(db.Text)
	text = db.Column(db.Text)
	link = db.Column(db.String(255))
	document_date = db.Column(db.DateTime)
	president = db.Column(db.String(255))

	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

	def __init__(self, pid, title = None, text = None, link = None, document_date = None, president = None):
		self.pid = pid
		self.title = title
		self.text = text
		self.link = link
		self.document_date = document_date
		self.president = president

	def to_json(self):
		output = self.__dict__
		for key in output:
			if isinstance(output[key], datetime.datetime):
				output[key] = str(output[key])
		output.pop('_sa_instance_state')

		return output