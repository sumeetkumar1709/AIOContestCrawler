import requests
from bs4 import BeautifulSoup
import re

from utils import DbActions

class ContestCrawler:
    def __init__(self, platform_name,type):
        self.dbActions = DbActions()
        self.cls = 'ContestCrawler'
        self.contests = None  # Initialize an instance variable to hold contests
        
        if type == 'fetch':
            self.contests = self.get_contests(platform_name)
        elif type == 'crawl':
            if hasattr(self, platform_name):
                return getattr(self, platform_name)()  # Call the method named after the platform
            else:
                raise ValueError(f"No method found for platform: {platform_name}")
            
    def codeforces(self):
        try:
            print("Crawling Codeforces...")
            session = requests.Session()
            session.get('https://codeforces.com/contests')
            response = session.get('https://codeforces.com/api/contest.list?')
            response = response.json()['result']
            response = [x for x in response if x['phase'] == 'BEFORE']
            self.dbActions.insert_codeforces(response)
        except Exception as e:
            print(e)

    def codechef(self):
        try:
            print("Crawling CodeChef...")
            session = requests.Session()
            response = session.get('https://www.codechef.com/contests')

            # Extract CSRF token from the response
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token_script = soup.find('script', text=re.compile('window.csrfToken'))
            csrf_token = re.search(r'window.csrfToken = "(.*?)";', csrf_token_script.string).group(1)

            session.headers.update({'X-CSRF-Token': csrf_token})
            params = {
                'sort_by': 'START',
                'sorting_order': 'asc',
                'offset': '0',
                'mode': 'all',
            }
            response = session.get('https://www.codechef.com/api/list/contests/all', params=params)
            response = response.json()['future_contests']
            self.dbActions.insert_codechef(response)
        except Exception as e:
            print(e)
    
    def gfg(self):
        try:
            print("Crawling GFG...")
            session = requests.Session()
            headers = {
                'accept': '*/*',
                'accept-language': 'en,en-US;q=0.9',
                'cache-control': 'no-cache',
                'origin': 'https://www.geeksforgeeks.org',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://www.geeksforgeeks.org/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            }
            session.headers.update(headers)
            params = {
                'page_number': '1',
                'sub_type': 'all',
                'type': 'contest',
            }
            response = session.get('https://practiceapi.geeksforgeeks.org/api/vr/events/', params=params)
            response = response.json()['results']['upcoming']
            self.dbActions.insert_gfg(response)
        except Exception as e:
            print(e)
            
            
    def get_contests(self,platform_name):
        self.contests  = self.dbActions.fetch_data_by_platform(platform_name)
        return self.contests  
