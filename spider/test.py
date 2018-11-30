import re
import requests

url = 'https://book.qidian.com/info/1004608738#Catalog'

r = requests.get(url = url)
print r.text