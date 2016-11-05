from lxml import html
import requests
import json
import time
import sys

"""
Debate

A class to access data about a single debate.
"""
class Debate():

    """
    __init__

    Initialize object with an id that can be retrieved from a Deletes class.
    """
    def __init__(self, id):
        self.id = id
        self.data = []
        self.retrieve()

    """
    retrieve

    Return the debate.
    """
    def retrieve(self):

        url = 'http://www.presidency.ucsb.edu/ws/index.php?pid='

        page = requests.get(url + str(self.id))
        tree = html.document_fromstring(page.text)

        self.data = {
            "text": tree.xpath('//span[@class="displaytext"]')[0].text_content()
        }

        return self.data

    """
    words

    Return the (approximate) number of words in this debate.
    """
    def words(self):
        return len(self.data["text"].split(" "))
