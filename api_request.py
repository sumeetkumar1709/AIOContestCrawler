import requests

def hit_api():
    url = "https://aio-contest-crawler.vercel.app/force-run-task" 
    response = requests.post(url)

    if response.status_code == 200:
        print("API hit successfully:", response.json())
    else:
        print("Failed to hit API:", response.status_code)

if __name__ == "__main__":
    hit_api()
