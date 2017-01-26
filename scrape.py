import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from lib.scraper import Scraper
Scraper.scrape(True)
