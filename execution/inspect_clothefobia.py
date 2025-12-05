
import os
import json
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

def main():
    api_token = os.getenv("APIFY_TOKEN")
    client = ApifyClient(api_token)
    
    # Test "clothefobia/linkedin-people-search" (or whatever the ID is)
    # I'll try to find the ID via search results or just guess standard names
    # Search result [1] said "clothefobia/linkedin-people-search"
    
    actor_id = "clothefobia/linkedin-people-search" 
    
    print(f"Testing {actor_id} with keywords...")
    run_input = {
        "keywords": "Software Engineer",
        "location": "United States",
        "limit": 1
    }
    
    try:
        run = client.actor(actor_id).call(run_input=run_input)
        if run:
            print(f"SUCCESS. Dataset: {run['defaultDatasetId']}")
            items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
            if items:
                 print("Keys:", list(items[0].keys()))
            return
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    main()
