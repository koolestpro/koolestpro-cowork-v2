#!/usr/bin/env python3
"""
relevance_filter.py — light relevance + brand-safety pass for koolestpro-trend-radar.

Runs BEFORE anything reaches the Tips topic shortlist or the Format Radar card,
per Step 11's "a light relevance/brand-safety filter runs before anything reaches
the shortlist... so off-brand or irrelevant finds don't waste review time" rule.

This is deliberately simple (keyword/heuristic, not a model call) — it's a coarse
pre-filter, not the final judgment. Ridwan still reviews everything downstream
(Tips carousel before it posts, Format Radar card before he acts on it). The goal
here is just to stop obvious noise from reaching him, not to be a perfect judge.

Usage as a library:
    from relevance_filter import filter_items

    kept = filter_items(
        items,                       # list of dicts with a "text" (or "title") field
        niche_keywords=[...],        # from trend-radar-config.json
        avoid_terms=[...],           # brand-safety blocklist
        min_keyword_hits=1,
    )
"""

import re

DEFAULT_AVOID_TERMS = [
    # Generic brand-safety blocklist — politically/religiously charged or otherwise
    # off-brand terms that shouldn't drive a CRO/web-design professional's content,
    # regardless of how much engagement they're getting. Project-specific config
    # (trend-radar-config.json) can extend this list per project/niche.
    "election", "president", "war", "conflict", "shooting", "died", "death",
    "nsfw", "onlyfans", "crypto scam", "get rich quick",
]


def _text_of(item):
    return (item.get("text") or item.get("title") or item.get("description") or "").lower()


def _keyword_hits(text, keywords):
    return sum(1 for kw in keywords if kw.lower() in text)


def _has_avoid_term(text, avoid_terms):
    return any(term.lower() in text for term in avoid_terms)


def filter_items(items, niche_keywords, avoid_terms=None, min_keyword_hits=1):
    avoid_terms = avoid_terms if avoid_terms is not None else DEFAULT_AVOID_TERMS
    kept = []
    for item in items:
        text = _text_of(item)
        if not text:
            continue
        if _has_avoid_term(text, avoid_terms):
            continue
        hits = _keyword_hits(text, niche_keywords)
        if hits < min_keyword_hits:
            continue
        item = dict(item)
        item["relevance_hits"] = hits
        kept.append(item)
    # Relevance-weighted, but preserve the caller's own engagement ranking as the
    # primary sort key — relevance is a gate here, not a re-ranking signal, since
    # engagement is what actually indicates "trending", relevance just confirms
    # it's on-topic.
    return kept


if __name__ == "__main__":
    import json
    import sys

    raw = json.load(sys.stdin)
    keywords = raw.get("niche_keywords", [])
    avoid = raw.get("avoid_terms")
    items = raw.get("items", [])
    result = filter_items(items, keywords, avoid, raw.get("min_keyword_hits", 1))
    print(json.dumps({"kept": result, "kept_count": len(result), "input_count": len(items)}, indent=2))
