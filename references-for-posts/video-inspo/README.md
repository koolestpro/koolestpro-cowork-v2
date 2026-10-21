# video-inspo: saved TikTok + Instagram videos (offline reference library)

Purpose: Ridwan's saved inspiration for the video/Reels version of the content automation. Everything here lives on disk so any AI tool can read it later. Nothing depends on the cloud.

## Folders
| Folder | What goes in | How it gets there |
|---|---|---|
| `tiktok/` | Videos, thumbnails, captions (`.info.json`) from the TikTok collection "koolestpro inspo" | Run `scripts/download_tiktok_inspo.sh` in Mac Terminal (needs Chrome logged in to TikTok, because the collection is private) |
| `instagram-screenrecs/` | Instagram saved reels, as screen recordings or screenshots Ridwan makes himself | Manual only. Project rule: no automation, scraping or downloaders on instagram.com (see `docs/system/instagram-warning-investigation-2026-09-18.md`) |
| `catalog.md` | One row per video: hook, format, difficulty tier, how we would automate it | Fill after download (template inside) |

## Source links
- TikTok collection: https://www.tiktok.com/@koolestpro/collection/koolestpro%20inspo-7690569627997932309
- Instagram saved folder "content-creation": https://www.instagram.com/koolestpro/saved/content-creation/18017107637787180/ (open by hand only)

## Status (2026-10-19)
- [x] Folder structure + downloader script written
- [ ] TikTok download run (the cloud session could not reach the private collection; automated Chrome control dropped)
- [ ] Catalog filled (needs the files on disk)
- [ ] Instagram: Ridwan screen-records 10-20 saved reels into `instagram-screenrecs/`, each with a one-line `why.md`
