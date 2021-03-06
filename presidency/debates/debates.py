from lxml import html
import requests
import json
import time
import sys

"""
Debates

A class to access data about debates at a high level.
"""
class Debates():

    """
    __init__

    Initialize by retrieving all data.
    """
    def __init__(self):
        self.data = None
        self.all()

    """
    all

    Return an array of dicts containing data about all presidential debates.
    """
    def all(self):

        url = "http://www.presidency.ucsb.edu/debates.php"

        # Retrieve all debates as tree.
        page = requests.get(url)
        tree = html.document_fromstring(page.text)

        # List of all debate and date elements.
        dates = [x for x in tree.xpath('//td[@class="docdate"]') if len(x.text_content()) > 0]
        debates = tree.xpath('//td[@class="doctext"]')

        # Throw error if lengths are off.
        if len(dates) != len(debates):
            raise Exception('Sorry - something went wrong! Please open an issue at https://github.com/jayrav13/presidency/issues and include the following timestamp: %s' % str(time.time()))
            return None

        # Curate list of all debates.
        self.data = []

        for i in range(0, len(debates)):

            self.data.append({
                "date" : dates[i].text_content(),
                "debate" : debates[i].xpath('a')[0].text_content(),
                "link" : debates[i].xpath('a')[0].attrib['href'],
                "id" : int(debates[i].xpath('a')[0].attrib['href'].split('?')[1].split('=')[1])
            })

        return self.data

    """
    count

    Return number of debates.
    """
    def count(self):
        return len(self.data)


