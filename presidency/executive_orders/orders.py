from lxml import html
import requests
import json
import time
import sys
from year import Year

"""
Orders

Get a list of all Executive Orders for a given year.
"""
class Orders():

    def __init__(self, year=-1):
        years = Year.all()

        if year not in years:
            self.year = max(years)
            raise Exception('Invalid year. Use presidency.executive_orders.year to find all valid years.')

        self.year = year

    def all(self):

        url = "http://www.presidency.ucsb.edu/executive_orders.php?year=%d&Submit=DISPLAY" % self.year

        page = requests.get(url)
        tree = html.document_fromstring(page.text)

        table = tree.xpath('//form[@name="executive_orders"]')[0].getnext().xpath('tr')

        output = []

        for i in range(1, len(table)):

            data = table[i].xpath('td')

            output.append({
                "president": data[0].text_content(),
                "date": data[1].text_content(),
                "id": data[2].xpath('a')[0].attrib['href'].split('=')[1],
                "link": "http://www.presidency.ucsb.edu" + data[2].xpath('a')[0].attrib['href'][2:]
            })

        return output
