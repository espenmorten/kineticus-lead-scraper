#!/usr/bin/env python3
"""
Scrape Leads
Wraps Apify `code_crafter/leads-finder` to scrape B2B leads.
"""

import os
import sys
import json
import argparse
from warnings import filterwarnings

# Suppress warnings (optional, good for cleaner CLI output)
filterwarnings("ignore")

try:
    from apify_client import ApifyClient
except ImportError:
    print("Error: 'apify-client' not found. Please install it: pip install apify-client", file=sys.stderr)
    sys.exit(1)

from dotenv import load_dotenv

def scrape_leads(industry, location, job_titles, limit=100, output_file=None):
    """
    Scrapes leads using Apify peakydev/leads-scraper-ppe.
    Returns the list of items fetched.
    """
    load_dotenv()
    api_token = os.getenv("APIFY_TOKEN")
    
    if not api_token:
        raise ValueError("APIFY_TOKEN not found in .env")

    # Based on schema documentation for peakydev/leads-scraper-ppe
    # The actor requires a minimum of 1000 results
    # We will fetch 1000 but only save args.limit
    run_input = {
        "totalResults": 1000,
        "personCountry": [location], # e.g. "United States"
        "includeEmails": True,
    }

    if industry:
        # Map common terms to valid enums for this actor
        ind = industry
        if ind in ["SaaS businesses", "Computer Software", "Software"]:
            ind = "Software Development"
        run_input["industry"] = [ind]

    if job_titles:
        # Split by comma and strip whitespace if it's a string, otherwise assume list
        if isinstance(job_titles, str):
            titles = [t.strip() for t in job_titles.split(",")]
        else:
            titles = job_titles
        run_input["personTitle"] = titles

    print(f"DEBUG: run_input = {json.dumps(run_input, indent=2)}")

    try:
        client = ApifyClient(api_token)
        
        # Start the actor
        # Actor ID: peakydev/leads-scraper-ppe
        run = client.actor("peakydev/leads-scraper-ppe").call(run_input=run_input)
        
        # Check for success
        if not run:
            print("Error: Actor run failed (no run object returned).", file=sys.stderr)
            return []

        # Iterate through the dataset items
        dataset_items = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            if len(dataset_items) >= limit:
                break
            dataset_items.append(item)

        print(f"Fetched {len(dataset_items)} items.")

        if output_file:
            # Ensure dir exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(dataset_items, f, indent=2)
            print(f"Results saved to {output_file}")
            
        return dataset_items

    except Exception as e:
        print(f"Error during Apify execution: {e}", file=sys.stderr)
        return []

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Scrape leads using Apify")
    parser.add_argument("--industry", required=False, help="Target industry (e.g. 'SaaS businesses')")
    parser.add_argument("--location", required=True, help="Target location (e.g. 'United States')")
    parser.add_argument("--job_titles", required=False, help="Comma-separated job titles")
    parser.add_argument("--limit", type=int, default=100, help="Max leads to fetch")
    parser.add_argument("--output", required=True, help="Output JSON file path")

    args = parser.parse_args()
    
    try:
        scrape_leads(
            industry=args.industry,
            location=args.location,
            job_titles=args.job_titles,
            limit=args.limit,
            output_file=args.output
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
