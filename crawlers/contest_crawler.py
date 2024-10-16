import requests

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

    def get_contests(self,platform_name):
        self.contests  = self.dbActions.fetch_data_by_platform(platform_name)
        return self.contests  
