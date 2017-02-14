import sys
import requests
import json
from lxml import html

reload(sys)
sys.setdefaultencoding("utf-8")

print("Building data structure.")

from lib.scraper import Scraper
data = Scraper.build()

print("Building data structure complete.")

content = json.load(open('data/results3.json', 'r'))

for president in data.keys():
	for category in data[president].keys():
		for i in range(0, len(data[president][category])):

			if data[president][category][i]['content'] is not None:
				continue

			pid = data[president][category][i]['pid']

			if str(pid) in content:
				data[president][category][i]['content'] = content[str(pid)]
				print("Success: " + str(pid))
			else:
				print("Not Found: " + str(pid))

f = open("data/combined.json", "w")
f.write(json.dumps(data))
f.close()