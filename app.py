
from flask import Flask, render_template, request, send_file, Response
import os
import csv
import io
import json
from execution.scrape_leads import scrape_leads

app = Flask(__name__)

# Ensure .tmp directory exists for temporary storage if needed
os.makedirs(".tmp", exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        # Get form data
        industry = request.form.get('industry')
        location = request.form.get('location')
        job_titles = request.form.get('job_titles')
        limit = int(request.form.get('limit', 100))

        # Run scrape
        # We don't save to a file iteratively in the web flow, we just get the memory object
        # but to be safe and debuggable, let's save a temp file
        temp_file = f".tmp/web_scrape_{os.getpid()}.json"
        
        leads = scrape_leads(
            industry=industry,
            location=location,
            job_titles=job_titles,
            limit=limit,
            output_file=temp_file
        )

        # Filter valid leads (remove status messages/empty emails)
        valid_leads = []
        for lead in leads:
            if "message" in lead or not lead.get("email"):
                continue
            valid_leads.append(lead)

        # Generate CSV
        # Headers based on peakydev schema
        headers = ["firstName", "lastName", "email", "position", "organizationName", "organizationIndustry", "city", "country", "linkedinUrl"]
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        
        for lead in valid_leads:
            row = [
                lead.get('firstName', ''),
                lead.get('lastName', ''),
                lead.get('email', ''),
                lead.get('position', ''),
                lead.get('organizationName', ''),
                lead.get('organizationIndustry', ''),
                lead.get('city', ''),
                lead.get('country', ''),
                lead.get('linkedinUrl', '')
            ]
            writer.writerow(row)
        
        # Create response
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=leads.csv"}
        )

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
