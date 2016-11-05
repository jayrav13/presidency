from lxml import html
import requests
import json
import time
import sys

"""
Order

Return a specific Executive Order.
"""
class Order():

    def __init__(self, id):
        self.id = id
        self.url = 'http://www.presidency.ucsb.edu/ws/index.php?pid=%d' % self.id
        self.tree = None


    def get(self):

        page = requests.get(self.url)
        self.tree = html.document_fromstring(page.text)

        output = {
            "text" : self.tree.xpath('//span[@class="displaytext"]')[0].text_content(),
            "date": self.tree.xpath('//span[@class="docdate"]')[0].text_content(),
            "title": self.tree.xpath('//title')[0].text_content(),
            "id": self.id,
            "url": self.url,
            "president": self.tree.xpath('//title')[0].text_content().split(':')[0]
        }

        return output
