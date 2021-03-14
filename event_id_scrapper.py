from re import T
import requests
from bs4 import BeautifulSoup as bs

page = requests.get("http://ufcstats.com/statistics/events/completed?page=all")
parsed_content = bs(page.content, 'html.parser')
results = parsed_content.find_all('a', class_='b-link b-link_style_black', href=True)

for result in results:
    to_store = {}
    to_store['event_id'] = result['href'].split('/')[-1]
    to_store['event_name'] = result.text.strip()
    print(to_store)
