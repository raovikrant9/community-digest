# Daily scheduled task

Ask Claude (in the desktop app, on the Mac that will run it) to create a scheduled task with this prompt.
Pick a time when you're nearly always at your desk, so the Mac is awake.

```
Run my daily community digest using the community-digest skill (load it with the Skill tool and follow it exactly).

Deliver the finished digest with SendUserMessage so it reaches me.

If my Mac can't be reached (asleep, offline, or the Claude desktop app is closed), don't retry repeatedly.
Send one short SendUserMessage: "Your community digest couldn't run. Your Mac wasn't reachable. Run /community-digest when you're at your desk."

If only one source fails (Chrome not open, Slack logged out, extension permission prompt timed out),
still deliver the digest from the source that worked and say in one line what was skipped and why.

This is read-only: never send, post or react in any WhatsApp group or Slack channel.
```

Settings to ask for:
- Runs on **this computer** (it needs the Mac).
- **Push notification** when it finishes.

## Tips
- Keep the Mac from sleeping at that time, or schedule a wake: `sudo pmset repeat wakeorpoweron MTWRFSU 11:40:00`
- Set Chrome and WhatsApp to open at login (System Settings → General → Login Items).
- You can always run it by hand with `/community-digest`.
