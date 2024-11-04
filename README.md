# Contest Crawler API

This project is a web application built using FastAPI that crawls contest data from various competitive programming platforms like Codeforces, CodeChef, and GeeksforGeeks (GFG). The application provides an API to fetch and manage contest data, which is stored in a Supabase database.

## Features

- **Scheduled Crawling**: Automatically crawls contest data at regular intervals (Uses GitHub Actions).
- **Manual Trigger**: Allows manual triggering of the crawling process via an API endpoint.
- **Data Storage**: Stores contest data in a Supabase database.
- **API Endpoints**: Provides endpoints to fetch contest data and platform information. For detailed API documentation, visit [API Docs](https://aio-contest-crawler.vercel.app/docs).


## Frontend Application

A frontend application, [Algo Arena](https://algo-arena-beta.vercel.app/), has been built using this API. It provides a user-friendly interface to view and interact with the contest data.


## Project Structure

- `api/main.py`: Main FastAPI application file.
- `crawlers/contest_crawler.py`: Contains the logic for crawling contest data from different platforms.
- `utils/dbQueries.py`: Handles database interactions using Supabase.
- `api_request.py`: Script to manually trigger the crawling process.
- `files/platforms.json`: Configuration file listing supported platforms and their crawlers.

## Setup

### Prerequisites

- Python 3.8+
- Supabase account and project
- Environment variables set up in a `.env` file



### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/contest-crawler-api.git
   cd contest-crawler-api
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI application:

   ```bash
   uvicorn api.main:app --reload
   ```

## Usage

### API Endpoints

- **GET** `/platforms/{platform_name}`: Fetch information about a specific platform.
- **POST** `/force-run-task`: Manually trigger the crawling process.
- **GET** `/contest/data`: Retrieve contest data ordered by start date.

