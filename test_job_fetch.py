from job_fetcher import fetch_jobs
jobs = fetch_jobs("data analyst", "India", 3)
for j in jobs:
    print(j)