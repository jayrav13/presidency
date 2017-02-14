#!venv/bin/python
from presidency import app
import os

if __name__ == '__main__':
	app.run(debug=True, host=os.environ.get('HOST'), port=int(os.environ.get('PORT')))