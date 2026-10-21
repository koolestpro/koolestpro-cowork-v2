#!/bin/bash
# Downloads Ridwan's saved TikTok videos offline into the project. Run in Mac Terminal. TikTok only, never instagram.com.
# Mode A (try first): whole collection via your Chrome login.
# Mode B (fallback): put one video URL per line in tiktok/links.txt (see scripts/tiktok_collect_links.js), run again.
set -e
cd "$(dirname "$0")/../references-for-posts/video-inspo/tiktok"
command -v yt-dlp >/dev/null || brew install yt-dlp
OPTS=(--cookies-from-browser chrome --write-info-json --write-description --write-thumbnail
  --download-archive archive.txt -f "bv*[height<=1080]+ba/b" --merge-output-format mp4
  -o "%(upload_date)s_%(uploader)s_%(id)s/%(id)s.%(ext)s")
if [ -s links.txt ]; then yt-dlp "${OPTS[@]}" -a links.txt
else yt-dlp "${OPTS[@]}" "https://www.tiktok.com/@koolestpro/collection/koolestpro%20inspo-7690569627997932309"; fi
echo "Done: $(pwd)"
