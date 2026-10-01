# Desktop backup runner

The weekly cloud routine is the primary runner. Use this when the cloud is unavailable, or when you want to run a client on your own machine.

## One-off run
```bash
cd ~/path/to/koolestpro-cowork-v2
chmod +x seo/desktop/run-week.sh
./seo/desktop/run-week.sh tapandrate
```

## Schedule it (macOS, launchd)
Save as `~/Library/LaunchAgents/com.koolestpro.seo.tapandrate.plist`, change the two paths, then run `launchctl load ~/Library/LaunchAgents/com.koolestpro.seo.tapandrate.plist`.
Runs Mondays at 07:40. Your Mac must be awake. If it's asleep, launchd runs the job when it next wakes.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.koolestpro.seo.tapandrate</string>
  <key>ProgramArguments</key><array>
    <string>/bin/bash</string><string>-lc</string>
    <string>/Users/YOU/path/to/koolestpro-cowork-v2/seo/desktop/run-week.sh tapandrate</string>
  </array>
  <key>StartCalendarInterval</key><dict>
    <key>Weekday</key><integer>1</integer><key>Hour</key><integer>7</integer><key>Minute</key><integer>40</integer>
  </dict>
  <key>StandardOutPath</key><string>/tmp/seo-tapandrate.log</string>
  <key>StandardErrorPath</key><string>/tmp/seo-tapandrate.err</string>
</dict></plist>
```

## Linux / WSL (cron)
```
40 7 * * 1  cd /path/to/koolestpro-cowork-v2 && ./seo/desktop/run-week.sh tapandrate >> /tmp/seo-tapandrate.log 2>&1
```

## Don't double-run
If the cloud routine is active, keep the desktop schedule **unloaded** (`launchctl unload …`) and only use it manually. Two runs in the same week would create two Shopify drafts.
