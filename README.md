## presidency

[![PyPI version](https://badge.fury.io/py/presidency.svg)](https://badge.fury.io/py/presidency)

Welcome to `presidency`, a Python Wrapper for the [American Presidency Project](http://www.presidency.ucsb.edu). This package includes a variety of API's that scrape data from this project and provide helper functions for these data sets as well.

### Install

To install, execute `pip install presidency`.

### Usage

By navigating to `presidency/`, you will find a list of folders, each of which is a package of classes that scrapes different data. These classes can then be individually used and loaded. A simple example:

```python
from presidency.debates import Debates, Debate
```

Each folder has an individual `README.md` for usage.

### License

MIT License
