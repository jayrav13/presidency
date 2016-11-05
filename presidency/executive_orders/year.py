from lxml import html
import requests
import json
import time
import sys

"""
Year

A class to return all years for which Executive Orders are archived.
"""
class Year():

    """
    all

    Return a list of all years.
    """
    @staticmethod
    def all():

        page = requests.get('http://www.presidency.ucsb.edu/executive_orders.php')
        tree = html.document_fromstring(page.text)

        years = tree.xpath('//select[@id="year"]')[0].xpath('option')
        return [int(x.text_content()) for x in years]
