#!/usr/bin/env python3
"""Log one signal by hand (a Quora question, a LinkedIn post, a tweet, a job ad you spotted).

python outreach/scrapers/add_signal.py --domain coolsocks.co.uk --kind Question --source quora \
   --url https://www.quora.com/... --who "Sam, founder" --text "Asked why their checkout drops people"
kind: Question | Hiring | Feedback request | Launch | Complaint | Mention.  Add --normal to skip the hot priority.
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import directory_scrape as ds

ap = argparse.ArgumentParser()
ap.add_argument("--domain", default=""); ap.add_argument("--kind", default="Question"); ap.add_argument("--source", default="manual")
ap.add_argument("--url", default=""); ap.add_argument("--who", default=""); ap.add_argument("--text", required=True); ap.add_argument("--normal", action="store_true")
a = ap.parse_args()
row = {"domain": a.domain, "kind": a.kind, "source": a.source, "url": a.url, "who": a.who, "text": a.text}
if a.normal:
    row["urgency"] = "Normal"
print(ds.api_call(ds.load_env(), "add_signals", {"rows": [row]}))
