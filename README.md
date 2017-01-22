# presidency

Once a project for a [pip-installable Python package](http://pypi.python.org/pypi/presidency), **presidency** is a web scraping tool that sits atop the vast amount of data in the [American Presidency Project](http://presidency.ucsb.edu). It collects and indexes important data related to the Office of the President of the United States, such as Executive Orders and Proclamations issued.

## Getting Started

To get started, simply start with cloning this project and installing dependencies.

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

All of the classes required to collect data are in the `lib/scraper` folder. Launch the Python shell in Terminal:

```bash
$ python
Python 3.5.2 (default, Oct 11 2016, 04:59:56)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from lib.scraper import *
>>>
>>> ExecutiveOrderScraper.scrape()
>>> Executive Order retrieved: 121365
>>> Executive Order retrieved: 121366
>>> ...
>>> ...
```

The currently available classes include:

- `ExecutiveOrderScraper`
- `ProclamationScraper`

Every class has a static `.scrape()` method.

## Serve API

This project also includes a small but growing Flask API. Simply execute:

```bash
$ heroku local # or python app.py
```

...to get started. Below are the endpoints that you can hit.

| Method | URI | Parameters
|--------|-----|----------|
| `GET`    | `/api/v1/executive_orders` | |
| `GET`    | `/api/v1/proclamations`| |
