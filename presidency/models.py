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

	documents = db.relationship('Document', backref=db.backref('presidents'))

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

	documents = db.relationship('Document', backref=db.backref('document_categories'))

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

class Document(db.Model):
	"""
	Document

	A President / DocumentCategory Many-to-Many table to outline all documents.
	"""

	__tablename__ = 'documents'

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	pid = db.Column(db.Integer, unique=True, nullable=False)
	document_date = db.Column(db.DateTime)
	title = db.Column(db.Text)

	president_id = db.Column(db.Integer, db.ForeignKey('presidents.id'), nullable=False)
	document_category_id = db.Column(db.Integer, db.ForeignKey('document_categories.id'), nullable=False)

	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

	def __init__(self, pid, document_date, title):
		self.pid = pid
		self.document_date = document_date
		self.title = title

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

	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

	def __init__(self, title, uri, category_slug=None, category_name=None, document_date=None):
		self.title = title
		self.uri = uri
		self.category_slug = category_slug
		self.category_name = category_name
		self.document_date = datetime.datetime.strptime(document_date, "%B %d, %Y") if document_date != None else document_date

