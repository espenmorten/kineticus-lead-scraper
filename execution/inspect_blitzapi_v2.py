
import os
import json
import sys
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

def main():
    api_token = os.getenv("APIFY_TOKEN")
    client = ApifyClient(api_token)
    
    # Try Variation 1: searchType="people"
    print("Trying Variation 1: searchType='people'")
    run_input_1 = {
        "keyword": "Software Engineer",
        "location": "United States",
        "maxLeads": 1,
        "searchType": "people"
    }
    
    try:
        run = client.actor("blitzapi/linkedin-leads-scraper").call(run_input=run_input_1)
        if run:
            print(f"Variation 1 SUCCESS. Dataset: {run['defaultDatasetId']}")
            items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
            if items:
                 print("Keys:", list(items[0].keys()))
            return
    except Exception as e:
        print(f"Variation 1 Failed: {e}")

    # Try Variation 2: mode="people"
    print("\nTrying Variation 2: mode='people'")
    run_input_2 = {
        "keyword": "Software Engineer",
        "location": "United States",
        "maxLeads": 1,
        "mode": "people"
    }
    
    try:
        run = client.actor("blitzapi/linkedin-leads-scraper").call(run_input=run_input_2)
        if run:
            print(f"Variation 2 SUCCESS. Dataset: {run['defaultDatasetId']}")
            items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
            if items:
                 print("Keys:", list(items[0].keys()))
            return
    except Exception as e:
        print(f"Variation 2 Failed: {e}")

if __name__ == "__main__":
    main()
