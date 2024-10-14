import os
from fastapi import FastAPI, HTTPException, Header

from crawlers import ContestCrawler

app = FastAPI()

import json

# Load platforms configuration from a JSON file
with open('files/platforms.json', 'r') as f:
    platforms = json.load(f)


API_TOKEN = os.getenv('API_TOKEN')


@app.get("/platforms/{platform_name}")
async def get_platform_info(platform_name: str, x_api_token: str = Header(...)):
    try:
        # Check if the provided token matches the expected token
        if x_api_token != API_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid API token")

        platform_info = platforms.get(platform_name)
        if platform_info and  'ContestCrawler' in platform_info['crawlers']:
            return ContestCrawler(platform_name)
        raise HTTPException(status_code=404, detail="Platform not found")
    
    except Exception as e:
        print(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
