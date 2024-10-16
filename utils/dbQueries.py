import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class DbActions():
    def __init__(self) -> None:
        self.cls = 'DBQUERIES'
        
    def get_con(self):
        try:
            # Constructing the Supabase URL using environment variables
            host: str = os.getenv("SUPABASE_HOST")
            db: str = os.getenv("SUPABASE_DB")
            key: str = os.getenv("SUPABASE_PWD")
            url: str = os.getenv("SUPABASE_URL")

            # Create Supabase client
            return create_client(url, key)   
        except Exception as e:
            print(e)
            return None
    
    def fetch_data_by_platform(self, platform_name):
        try:
            client = self.get_con()
            if client is None:
                return None  # Handle the case where the client could not be created

            # Fetch records from the contests table based on the platform name
            response = client.from_('contests').select('*').eq('platform', platform_name).execute()
            return response.data  # Return the fetched data
        except Exception as e:
            print(e)
            return None  # Return None in case of an error
        finally:
            # No explicit close needed, but you can log or handle cleanup if necessary
            pass

    def insert_codeforces(self, data=[]):
        try:
            masterList = []
            for row in data:
                temp =  []
                temp.append(row.get('id'))
                temp.append(row.get('name'))
                temp.append(row.get('durationSeconds'))
                temp.append('codeforces')
                start_time = row.get('startTimeSeconds') or 0
                start_time = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d')
                temp.append(start_time)
                temp = tuple(temp)
                masterList.append(temp)
            
            if len(masterList) > 0:
                client = self.get_con()
                if client is None:
                    return  # Handle the case where the client could not be created
                
                # Delete existing records with the same platform
                client.from_('contests').delete().match({
                    'platform': 'codeforces'
                }).execute()

                # Prepare the data for insertion
                data_to_insert = []
                for tpl in masterList:
                    data_to_insert.append({
                        'contest_id': tpl[0],
                        'name': tpl[1],
                        'duration': tpl[2],
                        'platform': 'codeforces',
                        'start_date': tpl[4]
                    })

                # Log the data to be inserted for debugging
                print(f"Inserting data: {data_to_insert}")

                # Insert the data into the public.contests table
                response = client.from_('contests').insert(data_to_insert).execute()
        except Exception as e:
            print(e)
        finally:
            # No explicit close needed, but you can log or handle cleanup if necessary
            pass
