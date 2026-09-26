---
name: abuzaid-saturday-batch
description: Weekly Saturday batch — draft 21 posts (3/day), push TEXT to Google Sheets; images are reviewed 3-by-3 separately
---

You are running the weekly Abu Zayd ar-Rāghib Saturday content batch. The user is not present; run autonomously and end with a report. Do not post anything to Facebook. Do NOT generate images in this run — images are reviewed separately, three at a time, with Ridwan.

## CONTEXT
- Persona: Abu Zayd ar-Rāghib, a Nigerian Muslim intellectual on Facebook
- Brand rules: /Users/mac/Downloads/Islamic Content/CLAUDE.md (read Section 0 in full)
- Skill: /Users/mac/Downloads/Islamic Content/abuzaid-content-engine/SKILL.md
- References (in abuzaid-content-engine/references/): voice-persona.md, image-guide.md, image-memory.md, people-reference.md, opposing-outlets.md
- Outputs folder: /Users/mac/Downloads/Islamic Content/abuzaid-content-engine/outputs/
- Review Queue sheet: https://docs.google.com/spreadsheets/d/1pxQVNnaRlvuL_fP4zT7xQ47M1-HSaIR1hN05xAFvcsA/edit

## STEP 1: Check if this week's batch file exists
Compute the coming Monday (two days after today) as MONDAY_DATE (YYYY-MM-DD). Expected file:
  /Users/mac/Downloads/Islamic Content/abuzaid-content-engine/outputs/week-of-MONDAY_DATE-posts.md
- If it EXISTS: print "Batch file already found for MONDAY_DATE, skipping draft." Go to Step 3.
- If it does NOT exist: continue to Step 2.

## STEP 2: Draft the week (only if the file is missing)
Read CLAUDE.md Section 0 in full, then SKILL.md, then run the abuzaid-content-engine skill in weekly batch mode.
- 21 posts: 3 per day (Morning, Afternoon, Evening), Monday through Sunday.
- Do all content writing on Claude Sonnet (spawn subagents with model "sonnet"); Opus only orchestrates, inspects, and compiles. Never write final post copy on Opus.
- Apply the humanizer to every post.
- For each post include: weekday, date, slot, pillar, mode, posting time, the humanized post, WORD COUNT, LONGEST PARAGRAPH, and the UPDATED IMAGE PROMPT only. Do NOT produce an ORIGINAL comparison prompt.
- Use this exact section header format (the slot name must appear in the header so the pipeline can detect it):
  ## Monday, June 29, 2026 — Morning (7:00 AM)
  ## Monday, June 29, 2026 — Afternoon (2:00 PM)
  ## Monday, June 29, 2026 — Evening (8:30 PM)
- Save to /Users/mac/Downloads/Islamic Content/abuzaid-content-engine/outputs/week-of-MONDAY_DATE-posts.md.

## STEP 3: Push TEXT to the Review Queue (no images)
Create the logs dir if missing:
  mkdir -p "/Users/mac/Downloads/Islamic Content/logs"
Push every post's text to the sheet as DRAFT, image column left empty:
  cd "/Users/mac/Downloads/Islamic Content" && python3 abuzaid-3by3-review.py text 2>&1 | tee "/Users/mac/Downloads/Islamic Content/logs/batch-$(date +%Y-%m-%d).log"
(Equivalent fallback if needed: python3 abuzaid-saturday-batch.py --no-images)
If a dependency is missing: pip3 install gspread google-auth requests --break-system-packages, then retry.
Do NOT generate or attach images in this run.

## STEP 4: Report
1. Whether the draft was generated fresh or an existing file was used
2. Which week was processed (Monday date through Sunday date)
3. How many posts were pushed to the sheet (expect 21)
4. Any errors or warnings from the log
5. Review link: https://docs.google.com/spreadsheets/d/1pxQVNnaRlvuL_fP4zT7xQ47M1-HSaIR1hN05xAFvcsA/edit
6. Reminder to Ridwan: "Text is in the Review Queue. Images are next: in a Cowork chat we run the 3-by-3 review — I generate each day's 3 images for you to approve, then attach them to the sheet (abuzaid-3by3-review.py gen, then attach). Mark posts APPROVED before Make.com posts at 7:00 AM, 2:00 PM, and 8:30 PM WAT."