import requests

class ContestCrawler:
    def __init__(self, platform_name):
        self.cls = 'ContestCrawler'
        self.contests = None  # Initialize an instance variable to hold contests
        if platform_name == 'codeforces':
            self.contests = self.Codeforces()  

    def Codeforces(self):
        try:
            session = requests.Session()
            session.get('https://codeforces.com/contests')
            response = session.get('https://codeforces.com/api/contest.list?')
            response = response.json()['result']
            response = [x for x in response if x['phase'] == 'BEFORE']
            return response  # Return the response as desired
        except Exception as e:
            print(e)

    def get_contests(self):
        return self.contests  # Method to retrieve contests
