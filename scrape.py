import sys
import requests
import json
from lxml import html

reload(sys)
sys.setdefaultencoding("utf-8")

print("Building data structure.")

from lib.scraper import Scraper
data = Scraper.build()

print("Data structure built.")

presidents = data.keys()

if len(sys.argv) == 3:
	presidents = presidents[ int(sys.argv[1]) : int(sys.argv[2]) ]
	print([x for x in presidents])

for president in data.keys():

	print("Starting with President " + president)

	for category in data[president].keys():

		print("Starting with category " + category)

		for i in range(0, len(data[president][category])):

			try:
				response = requests.get('http://www.presidency.ucsb.edu/ws/index.php?pid=' + str(data[president][category][i]['pid']))
				tree = html.document_fromstring(response.text)

				data[president][category][i]['content'] = tree.xpath('//span[@class="displaytext"]')[0].text_content()
				data[president][category][i]['error'] = None

				print("SUCCESS " + data[president][category][i]['title'])

			except Exception as e:
				data[president][category][i]['content'] = None
				data[president][category][i]['error'] = str(e)

				print("FAIL " + data[president][category][i]['title'])


		f = open('data/presidency-' + sys.argv[1] + '-' + sys.argv[2] + '.json', 'w')
		f.write(json.dumps(data))
		f.close()
		print("FILE WRITE")

	print(category)
	print(president)
