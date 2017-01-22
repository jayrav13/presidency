from presidency import app, db
import datetime

class President(db.Model):
	"""
	President

	All Presidents of the United States.
	"""

	__tablename__ = 'presidents'

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(255))
	number = db.Column(db.Integer, unique=True)

	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

	def __init__(self, name, number):
		self.name = name
		self.number = number

	def to_json(self):
		output = self.__dict__
		for key in output:
			if isinstance(output[key], datetime.datetime):
				output[key] = str(output[key])
		output.pop('_sa_instance_state')

		return output

class DocumentCategory(db.Model):
	"""
	DocumentCategory

	Written, Oral, etc. + subcategories.
	"""

	__tablename__ = 'document_categories'

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	full_text = db.Column(db.String(255))
	number = db.Column(db.Integer, unique=True)
	type = db.Column(db.String(255))
	category = db.Column(db.String(255), nullable=True)
	subcategory = db.Column(db.String(255), nullable=True)

	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

	def __init__(self, full_text, number, type, category = None, subcategory = None):
		self.full_text = full_text
		self.number = number
		self.type = type
		self.category = category
		self.subcategory = subcategory

	def to_json(self):
		output = self.__dict__
		for key in output:
			if isinstance(output[key], datetime.datetime):
				output[key] = str(output[key])
		output.pop('_sa_instance_state')

		return output
