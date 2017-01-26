# presidency

`presidency` is a web service that collects and acts on data related to the US presidency, with a potential to expand further. This includes Executive Orders, Proclamations, Speeches, Legislation (Signed, Veto'd, Pending), Statements & Press Releases, etc.

Inspired initially by the [American Presidency Project](http://presidency.ucsb.edu), it now scrapes from the APP and WhiteHouse.gov.

It also includes scripts supporting client apps, such as a Twitter bot for real time updates on new documents released.

## Getting Started

To get started, simply start with cloning this project and installing dependencies. Note - this uses Python 3.

```bash
$ git clone git@github.com:jayrav13/presidency.git
$ cd presidency/
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Next, create a copy of the `.env.example` file:

```bash
$ cp .env.example .env
```

Populate the newly created environment file. Once complete, you should have everything you need to get started.

**NOTE**: If electing to use a SQLite database, be sure to use an absolute path versus relative path. It is recommended that PostgreSQL or MySQL are used.

## Collect Data

To set up your database, executive the following commands:

```bash
python migrate.py db init
python migrate.py db migrate
python migrate.py db upgdate
```

Execute the latter two lines every time a database change is made and you want to migrate those changes.

## American Presidency Project

The APP has collected almost over 120,000 documents pertaining to all elements of the US presidency. The scraper here focuses on (almost 60,000 at time of writing these docs) documents released by those who served as US president.

From the root of the project:

```bash
$ python
Python 2.7.12 (default, Oct 11 2016, 05:20:59)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from lib.scraper import Scraper
>>> Scraper.scrape()
```

The `scrape()` function will persist everything returned.

Next, execute `Scraper.build()` and all of this data will be returned in a `dict` data structure. To persist to a file, you can do the following:

```bash
$ python
Python 2.7.12 (default, Oct 11 2016, 05:20:59)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from lib.scraper import Scraper
>>> import json
>>> 
>>> f = open('results.json', 'w')
>>> f.write(json.dumps(Scraper.build()))
>>> f.close()
```

The resulting data structure takes the following form:

```json
{
    "Abraham Lincoln": {
        "Debates": [], 
        "Written": [], 
        "Oral": [
            {
                "category": "Address", 
                "document_date": "1861-03-04 00:00:00", 
                "pid": 25818, 
                "subcategory": "Inaugural", 
                "title": "Inaugural Address"
            }, 
            {
                "category": "Address", 
                "document_date": "1865-03-04 00:00:00", 
                "pid": 25819, 
                "subcategory": "Inaugural", 
                "title": "Inaugural Address"
            },
            ...
		],
		....
	},
	...
}
```

An example is available at `data/presidency.json`.

The final step is to visit the following URL, swapping in `{pid}` for the document of interest:

`http://www.presidency.ucsb.edu/ws/index.php?pid={pid}`

**TODO**: Either populate core data in JSON or write a Python function that returns content given a `pid`.

## API

Coming Soon.

### Credits
Thank you to the American Presidency Project for inspiring this project: http://www.presidency.ucsb.edu

Built by Jay Ravaliya

### License
MIT