import requests
import json
from bs4 import BeautifulSoup

url = "https://www.ambitionbox.com/overview/tcs-overview"
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}
response = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(response.text, 'html.parser')
data = json.loads(soup.find('script', id='__NEXT_DATA__').string)
page_data = data['props']['pageProps']
ratings = page_data.get('aggregatedRatingsData', {})

print("Factors keys:", ratings.keys() if isinstance(ratings, dict) else type(ratings))
# Let's inspect it deeper
print(json.dumps(ratings, indent=2))
