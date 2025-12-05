# Lead Generation Workflow

**Goal**: Scrape B2B leads from Apify, validate their relevance to a target industry, and upload approved leads to Google Sheets.

**Inputs**:
- `INDUSTRY`: Target industry (e.g., "Software", "Construction").
- `LOCATION`: Target location (e.g., "United States", "New York").
- `JOB_TITLES`: Comma-separated list of job titles (e.g., "CEO,CTO,Owner").
- `TOTAL_LEADS`: Total number of leads to scrape (e.g., 100).

**Tools/Scripts**:
- `execution/scrape_leads.py` - Scrapes leads using Apify `code_crafter/leads-finder`.
- `execution/validate_leads.py` - Validates leads against the target industry.
- `execution/upload_to_sheets.py` - Uploads leads to Google Sheets.

**Outputs**:
- Google Sheet URL with the new leads.

**Edge Cases**:
- **Low Match Rate (<80%)**: If the initial test run usually has poor quality, stop and ask the user to refine inputs.
- **API Errors**: Handle Apify or Google API rate limits or auth errors.

## Process Steps

1.  **Test Run (Calibration)**
    - Scrape a small sample (25 leads) to verify filter quality.
    - Command: `python execution/scrape_leads.py --industry "[INDUSTRY]" --location "[LOCATION]" --job_titles "[JOB_TITLES]" --limit 25 --output .tmp/leads_test.json`

2.  **Validation**
    - Check if the scraped leads actually match the target industry.
    - Command: `python execution/validate_leads.py --input .tmp/leads_test.json --target_industry "[INDUSTRY]" --threshold 0.8`
    - **Logic**:
        - If `valid_percentage >= 80%`: Proceed to Step 3.
        - If `valid_percentage < 80%`: **STOP**. Notify user to refine filters (e.g., be more specific with industry or job titles).

3.  **Full Run**
    - Scrape the remaining/full amount of leads.
    - Command: `python execution/scrape_leads.py --industry "[INDUSTRY]" --location "[LOCATION]" --job_titles "[JOB_TITLES]" --limit [TOTAL_LEADS] --output .tmp/leads_full.json`

4.  **Upload to Sheets**
    - Upload the valid leads to the Google Sheet.
    - Command: `python execution/upload_to_sheets.py --input .tmp/leads_full.json`

5.  **Final Output**
    - Provide the Google Sheet URL to the user.
