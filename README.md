# Opportunita Bot

Automated job finder bot that searches for frontend developer positions in Italy and sends results via Telegram.

## How it works

A **Claude Code Routine** runs every 6 hours and:

1. Reads the CV from `cv/hamed_cv.pdf` to understand skills and experience
2. Searches the web for frontend developer jobs in Italy posted in the last 6 hours
3. Filters results for relevant positions in Italian cities
4. Sends new job listings to Telegram (avoids duplicates via `sent_urls.json`)
5. Pushes a report to the `reports/` folder on GitHub

## Setup

1. Copy `.env.example` to `.env` and add your Telegram bot token:
   ```
   cp .env.example .env
   ```

2. Configure the Claude Code routine to run on a 6-hour schedule

## Telegram message format

```
🟢 *Job Title*
🏢 Company Name
📍 Location
🔗 https://link-to-job
```

## Project structure

```
cv/hamed_cv.pdf          # CV file
reports/                  # Auto-generated job search reports
.env                      # Telegram bot token (not tracked)
sent_urls.json            # Duplicate tracking (not tracked)
CLAUDE.md                 # Instructions for Claude Code routine
```
