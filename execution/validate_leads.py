#!/usr/bin/env python3
"""
Validate Leads
Checks if scraped leads match the target industry.
Ideal: Use LLM for semantic matching.
Fallback: Keyword matching.
"""

import os
import sys
import json
import argparse
from typing import List, Dict

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def validate_lead_keyword_mode(lead: Dict, target_industry: str) -> bool:
    """
    Simple keyword validation.
    Checks if target industry words appear in the lead's industry field.
    """
    lead_industry = str(lead.get('industry', '')).lower()
    company_desc = str(lead.get('company_description', '')).lower()
    target = target_industry.lower()
    
    # Split target into keywords to be more permissive
    keywords = target.split()
    
    for kw in keywords:
        if kw in lead_industry or kw in company_desc:
            return True
            
    return False

def main():
    parser = argparse.ArgumentParser(description="Validate scraped leads.")
    parser.add_argument("--input", required=True, help="Input JSON file path with leads")
    parser.add_argument("--target_industry", required=True, help="Target industry name")
    parser.add_argument("--threshold", type=float, default=0.8, help="Pass threshold (0.0 - 1.0)")
    
    args = parser.parse_args()

    # 1. Load Data
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            leads = json.load(f)
    except Exception as e:
        print(f"Error loading input file: {e}", file=sys.stderr)
        sys.exit(1)

    if not leads:
        print("Warning: No leads found in input file.")
        print(json.dumps({"valid_percentage": 0.0, "total": 0, "valid_count": 0}))
        return

    # 2. Validate
    # TODO: If OPENAI_API_KEY or similar is present, we could swap this for an LLM call
    # for higher fidelity verification.
    
    valid_leads = []
    
    print(f"Validating {len(leads)} leads against industry '{args.target_industry}'...")
    
    filtered_count = 0
    for lead in leads:
        # Filter status messages
        if "message" in lead or not lead.get("email"):
             continue
        filtered_count += 1

        # Helper to get field safely
        # Mapping for peakydev/leads-scraper-ppe
        industry = lead.get("organizationIndustry", "")
        job_title = lead.get("position", "")
        # ... logic continues ...
        
        # Check if industry matches (keyword based)
        industry_match = False
        if args.target_industry.lower() in industry.lower():
             industry_match = True

        # Check title
        title_match = bool(job_title)

        is_valid = industry_match and title_match
        
        if is_valid:
            valid_leads.append(lead)

    # 3. Calculate Stats
    total = filtered_count
    count = len(valid_leads)
    percentage = count / total if total > 0 else 0.0
    
    result = {
        "valid_percentage": percentage,
        "total": total,
        "valid_count": count,
        "passed_threshold": percentage >= args.threshold
    }

    # 4. Output
    print(json.dumps(result, indent=2))
    
    # Optional: Save filtered leads? 
    # For now, just output stats as requested by the workflow logic logic.

if __name__ == "__main__":
    main()
