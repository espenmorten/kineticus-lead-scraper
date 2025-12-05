
import os
import json
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

def main():
    api_token = os.getenv("APIFY_TOKEN")
    client = ApifyClient(api_token)
    
    # Test "blitzapi/linkedin-leads-scraper"
    # Search for "Software Engineer" in "US"
    run_input = {
        "keyword": "Software Engineer",
        "location": "United States",
        "maxLeads": 1
    }
    
    print("Starting actor run...")
    run = client.actor("blitzapi/linkedin-leads-scraper").call(run_input=run_input)
    
    if not run:
        print("Run failed")
        return

    print(f"Run finished. Dataset: {run['defaultDatasetId']}")
    
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    if items:
        print("Sample Item Keys:", list(items[0].keys()))
        print(json.dumps(items[0], indent=2))
    else:
        print("No items found.")

if __name__ == "__main__":
    main()
