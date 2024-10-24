import os
from fastapi import FastAPI, HTTPException, Header
from apscheduler.schedulers.background import BackgroundScheduler  # Import BackgroundScheduler
from dotenv import load_dotenv

from crawlers import ContestCrawler
from utils import DbActions

load_dotenv()
app = FastAPI()

import json

# Load platforms configuration from a JSON file
with open('files/platforms.json', 'r') as f:
    platforms = json.load(f)


API_TOKEN = os.getenv('API_TOKEN')

# Initialize the scheduler
scheduler = BackgroundScheduler()

def scheduled_task():
    platform_list = list(platforms.keys())
    for plat in platform_list:
        ContestCrawler(plat,'crawl')
    print("Scheduled task executed") 

refresh_interval = os.getenv('REFRESH_INTERVAL')
# Schedule the task to run every hour
scheduler.add_job(scheduled_task, 'interval', minutes = int(refresh_interval))

def start_scheduler():
    scheduler.start()  

def shutdown_scheduler():
    scheduler.shutdown() 

app.add_event_handler("startup", start_scheduler)  # Register the startup event handler
app.add_event_handler("shutdown", shutdown_scheduler)  # Register the shutdown event handler

@app.get("/platforms/{platform_name}")
async def get_platform_info(platform_name: str, x_api_token: str = Header(...)):
    try:
        # Check if the provided token matches the expected token
        if x_api_token != API_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid API token")

        platform_info = platforms.get(platform_name)
        if platform_info and  'ContestCrawler' in platform_info['crawlers']:
            return ContestCrawler(platform_name,'fetch')
        raise HTTPException(status_code=404, detail="Platform not found")
    
    except Exception as e:
        print(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/force-run-task")
async def force_run_task():
    scheduled_task()  
    return {"message": "Scheduled task executed immediately."}


@app.get("/contest/data")
async def get_contest_data(x_api_token: str = Header(...)):
    try:
        # Check if the provided token matches the expected token
        if x_api_token != API_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid API token")

        data = DbActions().fetch_contests_ordered_by_start_date()
        return {"data": data}
    except Exception as e:
        print(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")