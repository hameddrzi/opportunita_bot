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

4. **Send each new job to Telegram** using the bot API (chat_id: `5134844472`). Read `TELEGRAM_BOT_TOKEN` from the `.env` file. Message format:
   ```
   🟢 *{title}*
   🏢 {company}
   📍 {location}
   🔗 {url}
   ```

5. **Update `sent_urls.json`** with the URLs you just sent to avoid duplicates on the next run.

6. **Create a report** in `reports/` named `report_YYYY-MM-DD_HH-MM.md` with a summary of what was found and sent.

7. **Push to GitHub**:
   ```
   git add reports/ sent_urls.json
   git commit -m "Job search report — {date}"
   git push origin master
   ```

## Important notes

- The Telegram bot token is in `.env` — never commit this file.
- Always check `sent_urls.json` before sending to avoid duplicate messages.
- If no new jobs are found, still create a report noting that, but don't send any Telegram messages.
