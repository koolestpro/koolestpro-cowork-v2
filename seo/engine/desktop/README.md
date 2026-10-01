# Desktop runner

Runs this project's weekly SEO cycle on your own machine with Claude Code. Each project folder runs its own engine with its own keys.

## One-off run
```bash
cd /path/to/your-project
chmod +x seo/engine/desktop/run-week.sh
./seo/engine/desktop/run-week.sh
```
Connectors you want in the run (Gmail drafts, Ubersuggest, image generation) must be connected in Claude Code on this machine. Add their tool names to `--allowedTools` in `run-week.sh` (e.g. `mcp__Gmail__create_draft`).

## Weekly schedule (macOS, launchd)
Save as `~/Library/LaunchAgents/com.seo-engine.<project>.plist`, change the path, then `launchctl load` it. Runs Mondays at 07:40. If the Mac is asleep, it runs when it next wakes.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.seo-engine.PROJECT</string>
  <key>ProgramArguments</key><array>
    <string>/bin/bash</string><string>-lc</string>
    <string>/Users/YOU/path/to/PROJECT/seo/engine/desktop/run-week.sh</string>
  </array>
  <key>StartCalendarInterval</key><dict>
    <key>Weekday</key><integer>1</integer><key>Hour</key><integer>7</integer><key>Minute</key><integer>40</integer>
  </dict>
  <key>StandardOutPath</key><string>/tmp/seo-PROJECT.log</string>
  <key>StandardErrorPath</key><string>/tmp/seo-PROJECT.err</string>
</dict></plist>
```

## Linux / WSL (cron)
```
40 7 * * 1  cd /path/to/PROJECT && ./seo/engine/desktop/run-week.sh >> /tmp/seo-PROJECT.log 2>&1
```

If a cloud routine also runs this project, leave the desktop schedule unloaded. The SOP's double-run guard stops a second Shopify draft in the same week, but there's no reason to run both.
