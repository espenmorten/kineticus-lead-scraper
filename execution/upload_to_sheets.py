#!/usr/bin/env python3
"""
Upload to Sheets
Uploads a JSON list of leads to a Google Sheet.
Requires: credentials.json and GOOGLE_SHEET_ID in .env
"""

import os
import sys
import json
import argparse
from warnings import filterwarnings

filterwarnings("ignore")

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
except ImportError:
    print("Error: Google API libs not found. Try: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib", file=sys.stderr)
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    parser = argparse.ArgumentParser(description="Upload leads to Google Sheets.")
    parser.add_argument("--input", required=True, help="Input JSON file path with leads")
    parser.add_argument("--overwrite", action="store_true", help="Clear sheet before uploading")
    
    args = parser.parse_args()

    # 1. Validation
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        print("Error: GOOGLE_SHEET_ID not found in .env", file=sys.stderr)
        sys.exit(1)
        
    creds_path = "credentials.json"
    if not os.path.exists(creds_path):
        print(f"Error: {creds_path} not found.", file=sys.stderr)
        sys.exit(1)

    # 2. Load Data
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            leads = json.load(f)
    except Exception as e:
        print(f"Error loading input file: {e}", file=sys.stderr)
        sys.exit(1)

    if not leads:
        print("No leads to upload.")
        sys.exit(0)

    # 3. Prepare Rows
    # Headers for peakydev/leads-scraper-ppe
    headers = ["first_name", "last_name", "email", "job_title", "company_name", "industry", "location", "linkedin"]
    
    values = []
    # Add values
    for lead in leads:
        # Skip invalid
        if "message" in lead or not lead.get("email"):
            continue

        row = [
            lead.get("firstName", ""),
            lead.get("lastName", ""),
            lead.get("email", ""),
            lead.get("position", ""),
            lead.get("organizationName", ""),
            lead.get("organizationIndustry", ""),
            f"{lead.get('city', '')}, {lead.get('country', '')}",
            lead.get("linkedinUrl", "")
        ]
        values.append(row)

    # 4. Upload
    print(f"Uploading {len(values)} leads to Sheet ID: {sheet_id}...")
    
    try:
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        if args.overwrite:
            print("Clearing existing data...")
            sheet.values().clear(spreadsheetId=sheet_id, range="A:Z").execute()
            # If we cleared, we definitely need headers
            existing_header = []
        else:
            # Check if header exists (naive check: just read A1)
            result = sheet.values().get(spreadsheetId=sheet_id, range="A1").execute()
            existing_header = result.get('values', [])
        
        # If empty, prepend headers
        final_values = values
        if not existing_header:
            final_values = [headers] + values

        body = {
            'values': final_values
        }
        
        # Append to the sheet
        # 'valueInputOption': 'RAW' or 'USER_ENTERED'
        result = sheet.values().append(
            spreadsheetId=sheet_id,
            range="A1",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        updates = result.get('updates', {})
        print(f"{updates.get('updatedRows')} rows appended.")
        print(f"Link: https://docs.google.com/spreadsheets/d/{sheet_id}")

    except Exception as e:
        print(f"Error uploading to Google Sheets: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
