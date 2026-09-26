---
name: stock-footage
description: Searches Pexels and Pixabay for free stock photos and video b-roll to use in edits. Use this whenever the user needs stock footage, b-roll, or a stock photo for a video project — e.g. "find some b-roll of a city skyline," "I need a stock clip of rain for this edit," "grab a few stock photos of coffee shops." Both sources are free-tier with no billing risk. Requires a keys.env file with PEXELS_API_KEY and PIXABAY_API_KEY — if one isn't found, ask the user where their video-gen folder is or for the keys directly rather than failing silently.
---

# Stock Footage Search

Searches Pexels and Pixabay (both free, no subscription, generous rate
limits) for stock photos and video clips. Use for b-roll, background footage,
or reference images in a video project.

## Finding the API keys

1. Look for a `keys.env` file in the user's connected `video-gen` folder (or
   wherever they keep it — check the folder root first). Format:
   ```
   PEXELS_API_KEY=...
   PIXABAY_API_KEY=...
   ```
2. If no `keys.env` is found and the keys aren't already in the environment,
   ask the user for them, or ask them to point you at the folder that has
   `keys.env`. Don't guess or fabricate a key — the search will just fail
   with a clear "no API key" error in that case, which is fine, just surface
   it plainly rather than pretending the search ran.
3. Both keys are free-tier with nothing billable behind them, so it's fine
   to ask the user to paste them directly in chat if there's no keys.env
   handy yet.

## Running a search

```bash
python3 scripts/search_stock.py "<query>" --type video --source both --keys /path/to/keys.env --limit 5
```

- `--type`: `photo` or `video` (default `video`)
- `--source`: `pexels`, `pixabay`, or `both` (default `both`)
- `--limit`: results per source (default 5)

Output is JSON: for each source, a list of hits with `preview` (thumbnail
URL), `download_url` (direct file URL), and `page_url` (the source page,
useful for attribution if the user wants it — neither service legally
requires attribution, but it's good practice to keep the page_url around in
case the user wants to credit the creator).

## Downloading a chosen clip/photo

Once the user picks a result (or you pick the best match for their brief),
download it directly:

```bash
curl -L -o b_roll_01.mp4 "<download_url>"
```

## Tips

- Query in plain, concrete terms — "rain on window at night" works better
  than trying to be clever with search operators; neither API supports
  advanced query syntax.
- If one source comes back empty or thin, the other one might not — that's
  why `--source both` is the default. Compare and pick the better clip
  rather than committing to the first result.
- For b-roll used inside a longer edit (see the `video-review`/ffmpeg
  workflow), keep clips under ~1080p unless the final render specifically
  needs 4K — it keeps ffmpeg passes faster.
