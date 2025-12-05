# Setting up Google Service Account Credentials

To allow the agent to upload leads to your Google Sheet, you need a **Service Account Key**.

## 1. Create Service Account
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project (e.g., "Lead Scraper").
3.  Search for and select **"APIs & Services" > "Credentials"**.
4.  Click **"Create Credentials"** > **"Service Account"**.
5.  Name it (e.g., "scraper-bot") and click **"Create and Continue"**.
6.  (Optional) Grant "Editor" role, or skip (we only need Sheets access).
7.  Click **"Done"**.

## 2. Generate Key (JSON)
1.  In the Credentials list, click on the **Email** of the Service Account you just created (e.g., `scraper-bot@...`).
2.  Go to the **"Keys"** tab.
3.  Click **"Add Key"** > **"Create new key"**.
4.  Select **"JSON"** and click **"Create"**.
5.  A file will download. **Rename this file to `credentials.json`**.
6.  Move it to your project folder: `/Users/espenkm/agentic_workflows/credentials.json`.

## 3. Enable APIs
1.  Go to **"APIs & Services" > "Library"**.
2.  Search for **"Google Sheets API"** and click **"Enable"**.

## 4. Share the Sheet
1.  Open your `credentials.json` file and find the `"client_email"` field.
    - It looks like: `scraper-bot@project-id.iam.gserviceaccount.com`.
2.  Copy that email address.
3.  Go to your target Google Sheet.
4.  Click **"Share"** (top right).
5.  Paste the email address and give it **"Editor"** access.
6.  Click **"Send"** (uncheck "Notify people" if you want).

Once done, the agent will have permission to write to that specific sheet.
