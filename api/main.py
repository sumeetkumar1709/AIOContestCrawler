import os
from fastapi import FastAPI, HTTPException, Header
from apscheduler.schedulers.background import BackgroundScheduler  # Import BackgroundScheduler

from crawlers import ContestCrawler

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

# Schedule the task to run every hour
scheduler.add_job(scheduled_task, 'interval', hours = 1)

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

@app.get("/force-run-task")
async def force_run_task():
    scheduled_task()  
    return {"message": "Scheduled task executed immediately."}
