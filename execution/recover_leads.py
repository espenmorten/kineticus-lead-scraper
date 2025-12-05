
import os
import sys
import json
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

def main():
    api_token = os.getenv("APIFY_TOKEN")
    dataset_id = "kQvLwR9VWHfb7K1Ml" 
    
    if not api_token:
        print("No APIFY_TOKEN")
        sys.exit(1)
        
    client = ApifyClient(api_token)
    
    items = []
    print(f"Fetching items from dataset {dataset_id}...")
    for item in client.dataset(dataset_id).iterate_items():
        items.append(item)
        
    print(f"Total items found: {len(items)}")
    
    with open(".tmp/leads_recovered.json", "w") as f:
        json.dump(items, f, indent=2)

if __name__ == "__main__":
    main()
