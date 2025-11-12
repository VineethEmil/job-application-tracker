# Job Application Tracker Automation

A fully cloud-hosted automation system that fetches job listings, updates a live Google Sheet, and emails daily summaries — built using Python and GitHub Actions.


Summary

This project automates the job search → tracking → reporting cycle, enabling continuous job discovery and analytics without manual effort.
A plug-and-play model for anyone wanting a self-updating career intelligence system.

---

## Overview

This project automates the end-to-end job search process.  
Every 6 hours, it:
1. Fetches fresh job listings from the **Adzuna API**.
2. Appends only new jobs into a connected **Google Sheet tracker**.
3. Logs every run in `run_history.log`.
4. Emails a **summary digest** of job activity and errors.

All tasks run entirely on **GitHub Actions**, eliminating the need for local execution or manual scheduling.

---

## Features

 Feature                            Description 

  **Automated Execution**        Runs every 6 hours via GitHub Actions (`cron: 0 */6 * * *`) |
  **Google Sheets Sync**         Adds new jobs while skipping duplicates using a unique `Job_ID` |
  **Email Digest**               Sends twice-daily summaries (successes + errors) using secure Gmail app credentials |
  **Serverless Deployment**      Executes in the cloud — no PC, no Task Scheduler |
  **Secure Secrets**             API keys and credentials stored in GitHub Secrets |
  **Detailed Logs**              Every execution is logged in `run_history.log` for traceability |

---

##  Architecture

│ GitHub Actions (Every 6 hrs) │
└──────────────┬───────────────┘
│
▼
Python Scripts

 job_fetcher.py         │ → Fetch jobs from Adzuna API
 auto_update_jobs.py    │ → Deduplicate + update Google Sheet
 gsheet_client.py       │ → Authorize + connect to Google API
 email_digest.py        │ → Send summary emails

│
▼
Google Sheet Tracker
│
▼
Email Digest Report


---
 Configure Google Sheets API

Create a Service Account from Google Cloud Console.

Download the JSON key file.

Copy its entire contents into a GitHub Secret (see below).

 Configure GitHub Secrets

Navigate to Settings → Secrets and variables → Actions → New repository secret and add:
Secret Name	Description
ADZUNA_APP_ID	Your Adzuna API App ID
ADZUNA_APP_KEY	Your Adzuna API Key
GOOGLE_SHEETS_CREDENTIALS	Full JSON content from the service account key
SHEET_NAME	Name of your Google Sheet
MAIL_SENDER	Gmail address used to send summaries
MAIL_PASSWORD	Gmail App Password (not regular password)
MAIL_RECEIVER	Recipient email for digests


 Workflow Schedule

The system executes automatically every 6 hours (UTC):
00:00, 06:00, 12:00, 18:00 UTC
→ 05:30, 11:30, 17:30, 23:30 IST

You can also trigger it manually:

GitHub → Actions → Job Tracker Automation → Run workflow → main

 Email Digest Example

Subject: Job Tracker Digest — 2025-11-13 11:30
Body:

Job Tracker Update Summary (Last 12 Hours)
[2025-11-13 11:30:00] Added 3 new jobs.
[2025-11-13 17:30:00] Added 2 new jobs.
Digest email sent successfully.

Key Files

File	                            Description

auto_update_jobs.py	                Orchestrates job fetching + Google Sheet update
job_fetcher.py	                    Fetches job listings via Adzuna API
gsheet_client.py	                Handles Google Sheets authentication and updates
email_digest.py	                    Compiles and sends digest emails
.github/workflows/job_tracker.yml	GitHub Actions automation workflow

Built With

Python 3.10

GitHub Actions

gspread / oauth2client for Google Sheets API

requests for Adzuna API

smtplib for email

dotenv for config management

License

This project is open-source and free to use under the MIT License.

Author

Vineeth Emil
Building Flipkart minutes | Data & Operations Professional | Supply Chain Specialist