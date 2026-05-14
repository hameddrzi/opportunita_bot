# Opportunita Bot — Claude Code Routine

## What to do

You are a job search assistant. Every time this routine runs:

1. **Read the CV** from `cv/hamed_cv.pdf` and extract the candidate's skills, experience, and profile.

2. **Search the web** for frontend developer jobs in Italy posted in the last 6 hours. Use these queries:
   - "frontend developer React Italy"
   - "sviluppatore frontend junior Italia"
   - "junior web developer TypeScript Italy"

3. **Filter results**:
   - Only jobs located in Italian cities or marked as remote in Italy
   - Only jobs posted within the last 6 hours
   - Skip any URL already in `sent_urls.json`

4. **Skip Telegram** — do NOT try to call the Telegram API directly. A GitHub Action handles Telegram delivery automatically when the report reaches master.

5. **Update `sent_urls.json`** with the new URLs to avoid duplicates on the next run.

6. **Create a report** in `reports/` named `report_YYYY-MM-DD_HH-MM.md` with:
   - Each job found (title, company, location, URL) formatted as:
     ```
     🟢 *{title}*
     🏢 {company}
     📍 {location}
     🔗 {url}
     ```
   - Summary of how many jobs found and sent

7. **Push to GitHub via Pull Request** — do NOT use `git push` directly (it is blocked in this environment). Instead:
   - Use the GitHub MCP tool to create a new branch named `claude/report-YYYY-MM-DD-HH-MM`
   - Push the report file to that branch using the GitHub MCP `create or update file` tool
   - Create a Pull Request from that branch into `master`
   - A GitHub Action will auto-merge the PR and send the report to Telegram

## Important notes

- **NEVER use `git push`** — it is blocked. Always use GitHub MCP tools to create a branch and PR.
- **NEVER call the Telegram API** — it is blocked. The GitHub Action handles Telegram.
- The Telegram bot token is in `.env` — never commit this file.
- Always check `sent_urls.json` before sending to avoid duplicate messages.
- If no new jobs are found, still create a report noting that, but don't create a PR.
