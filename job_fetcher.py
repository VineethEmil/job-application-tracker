import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "your_app_id_here")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "your_app_key_here")


def fetch_jobs(keyword="data analyst", location="India", max_results=5):
    """Fetch job listings from Adzuna and return normalized job dictionaries."""
    base_url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": max_results,
        "what": keyword,
        "where": location,
        "content-type": "application/json"
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print("❌ API request failed:", response.status_code, response.text)
        return []

    data = response.json()
    jobs = []

    for job in data.get("results", []):
        company = job.get("company", {}).get("display_name", "N/A").strip()
        title = job.get("title", "N/A").strip()
        link = job.get("redirect_url", "").strip()
        location_name = job.get("location", {}).get("display_name", "Unknown").strip()

        # Normalize the link (optional)
        clean_link = re.sub(r'\?.*', '', link)

        job_data = {
            "Company": company,
            "Role": title,
            "Source": "Adzuna",
            "Application_Status": "Fetched",
            "Link": link,
            "Notes": location_name,
        }

        # Stable unique identifier (company + role + city)
        clean_id_base = f"{company}_{title}_{location_name}"
        job_data["Job_ID"] = re.sub(r'[^a-z0-9]', '', clean_id_base.lower())

        jobs.append(job_data)

    print(f"✅ {len(jobs)} jobs fetched for '{keyword}' in {location}")
    return jobs


if __name__ == "__main__":
    test_jobs = fetch_jobs("data analyst", "India", 3)
    for job in test_jobs:
        print(job["Job_ID"])
