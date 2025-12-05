
import os
import json
import sys
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

def main():
    api_token = os.getenv("APIFY_TOKEN")
    client = ApifyClient(api_token)
    
    # Try Variation 3: Empty company URL
    print("Trying Variation 3: Empty company URL")
    run_input_3 = {
        "keyword": "Software Engineer",
        "location": "United States",
        "maxLeads": 1,
        "company_linkedin_url": ""
    }
    
    try:
        run = client.actor("blitzapi/linkedin-leads-scraper").call(run_input=run_input_3)
        if run:
            print(f"Variation 3 SUCCESS. Dataset: {run['defaultDatasetId']}")
            return
    except Exception as e:
        print(f"Variation 3 Failed: {e}")

    # Try Variation 4: Queries array
    print("\nTrying Variation 4: queries list")
    run_input_4 = {
        "queries": ["Software Engineer"],
        "location": "United States",
        "maxLeads": 1
    }
    
    try:
        run = client.actor("blitzapi/linkedin-leads-scraper").call(run_input=run_input_4)
        if run:
            print(f"Variation 4 SUCCESS. Dataset: {run['defaultDatasetId']}")
            return
    except Exception as e:
        print(f"Variation 4 Failed: {e}")

if __name__ == "__main__":
    main()
