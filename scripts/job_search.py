import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone

SERPAPI_KEY = os.environ["SERPAPI_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = "5134844472"

QUERIES = [
    "frontend developer React Italy",
    "sviluppatore frontend junior Italia",
    "junior web developer TypeScript Italy",
    "React developer junior remote Italy",
]

SKILLS = [
    "react", "typescript", "javascript", "html", "css", "angular",
    "frontend", "front-end", "web developer", "ui", "ux", "figma",
    "react native", "spring boot", "rest api", "graphql", "node",
]

SENT_URLS_FILE = "sent_urls.json"


def load_sent_urls():
    if os.path.exists(SENT_URLS_FILE):
        with open(SENT_URLS_FILE) as f:
            return set(json.load(f))
    return set()


def save_sent_urls(urls):
    with open(SENT_URLS_FILE, "w") as f:
        json.dump(sorted(urls), f, indent=2)


def search_jobs(query):
    params = urllib.parse.urlencode({
        "engine": "google_jobs",
        "q": query,
        "location": "Italy",
        "hl": "it",
        "api_key": SERPAPI_KEY,
        "chips": "date_posted:today",
    })
    url = f"https://serpapi.com/search.json?{params}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Search error for '{query}': {e}")
        return {}


def is_relevant(job):
    text = (
        job.get("title", "") + " " +
        job.get("description", "") + " " +
        job.get("company_name", "")
    ).lower()
    return any(skill in text for skill in SKILLS)


def send_telegram(message):
    payload = json.dumps({
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }).encode()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
            if result.get("ok"):
                print(f"Telegram: sent OK")
            else:
                print(f"Telegram error: {result}")
    except Exception as e:
        print(f"Telegram send failed: {e}")


def make_job_id(job):
    title = job.get("title", "").strip()
    company = job.get("company_name", "").strip()
    return f"{title}|{company}".lower()


def main():
    sent_urls = load_sent_urls()
    all_jobs = {}
    now = datetime.now(timezone.utc)

    for query in QUERIES:
        print(f"Searching: {query}")
        data = search_jobs(query)
        for job in data.get("jobs_results", []):
            job_id = make_job_id(job)
            if job_id not in all_jobs and job_id not in sent_urls:
                all_jobs[job_id] = job

    relevant = []
    for job_id, job in all_jobs.items():
        if is_relevant(job):
            relevant.append((job_id, job))

    print(f"Found {len(all_jobs)} unique jobs, {len(relevant)} relevant")

    sent_count = 0
    for job_id, job in relevant:
        title = job.get("title", "N/A")
        company = job.get("company_name", "N/A")
        location = job.get("location", "N/A")

        apply_links = job.get("apply_options", [])
        link = apply_links[0]["link"] if apply_links else job.get("share_link", "")

        msg = (
            f"🟢 *{title}*\n"
            f"🏢 {company}\n"
            f"📍 {location}\n"
        )
        if link:
            msg += f"🔗 {link}"

        send_telegram(msg)
        sent_urls.add(job_id)
        sent_count += 1

    save_sent_urls(sent_urls)

    # Create report
    os.makedirs("reports", exist_ok=True)
    report_name = f"report_{now.strftime('%Y-%m-%d_%H-%M')}.md"
    report_path = f"reports/{report_name}"

    with open(report_path, "w") as f:
        f.write(f"# Job Search Report — {now.strftime('%Y-%m-%d %H:%M')} UTC\n\n")
        f.write(f"## Summary\n")
        f.write(f"- Queries: {len(QUERIES)}\n")
        f.write(f"- Total unique jobs found: {len(all_jobs)}\n")
        f.write(f"- Relevant jobs: {len(relevant)}\n")
        f.write(f"- Sent to Telegram: {sent_count}\n\n")

        if relevant:
            f.write("## Jobs Found\n\n")
            for job_id, job in relevant:
                title = job.get("title", "N/A")
                company = job.get("company_name", "N/A")
                location = job.get("location", "N/A")
                apply_links = job.get("apply_options", [])
                link = apply_links[0]["link"] if apply_links else ""
                f.write(f"### {title}\n")
                f.write(f"- **Company:** {company}\n")
                f.write(f"- **Location:** {location}\n")
                if link:
                    f.write(f"- **Link:** {link}\n")
                f.write("\n")
        else:
            f.write("No relevant jobs found in this run.\n")

    print(f"Report saved: {report_path}")
    print(f"::set-output name=report_path::{report_path}")


if __name__ == "__main__":
    main()
