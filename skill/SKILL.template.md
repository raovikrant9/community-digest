---
name: community-digest
description: Pull recent messages from my tracked WhatsApp groups and Slack channels and write a short digest of experiments and results, questions people are asking, and new tools. Use when I say /community-digest or ask for my community digest.
---

# Community digest

Source and updates: https://github.com/raovikrant9/community-digest

Pulls recent messages from the community chats listed in CONFIG and writes one digest.
Default window: last 24 hours. If I name a window ("last 48h", "since Friday"), use that.

**First, check CONFIG.** If it still has placeholder values (`"Group name one"`, `PASTE-DEVICE-ID`, `T0000000000`),
or the user asks to "set up", "add a source" or "fix my digest", run **Setup mode** instead of a digest.

## Setup mode

You are the setup guide. The user won't read docs. Handhold them through it in chat.

**Rules**
- **Check before you ask.** Detect what's already in place yourself (step A) and only ask about what you can't detect.
- **One step per message.** Give a single small action, in plain words, then wait for "done". Never paste a wall of steps.
- **Verify after each step**, by re-running the matching check. If it still fails, use the Troubleshooting table, not a repeat of the same instruction.
- **Keep it short and friendly.** No jargon (don't say "database", "API" or "deviceId" unless they ask). Use ✅ / ❌ / ⏭️ for the checklist.
- Skip anything for a source they don't want. If they only want WhatsApp, never mention Chrome.

### A. Silent pre-check (before your first message)
Run these quietly. Don't narrate them:
1. **Mac linked?** Are the remote-device tools present, and does get_device_info succeed? (Linked = Claude desktop app open on their Mac.)
2. **WhatsApp app synced?** device_list_dir on `~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared`.
   If it isn't connected yet, call device_request_folder_access on it, with the reason "To read your WhatsApp groups (read-only)".
   ✅ if `ChatStorage.sqlite` exists and was modified within ~12h. ⚠️ if it's older (app not opened lately). ❌ if missing.
3. **Chrome extension?** list_connected_browsers. ✅ if at least one is connected.
4. **Slack on the web?** Only if 3 is ✅: in each connected browser (ask which one if several, per the tool's rule), open a tab at
   `https://app.slack.com/client` and list logged-in workspaces (snippet S1). ✅ if at least one non-work community workspace is there.

### B. First message: checklist + disclaimer
Send one short message shaped like this, filling in the statuses from step A:

> Here's what this needs. I've checked what I can:
>
> ✅/❌ **Claude desktop app** open on your Mac
> ✅/⚠️/❌ **WhatsApp desktop app**, installed and synced *(for WhatsApp groups)*
> ✅/❌ **Claude in Chrome extension** *(for Slack)*
> ✅/❌ **Your Slack communities open in Chrome** *(for Slack)*
>
> Heads-up: it's read-only and never posts anything. It reads WhatsApp from your Mac's own copy (no bots on your account) and Slack through your logged-in browser. Images and voice notes aren't included. Digests contain other people's messages, so keep them to yourself.
>
> **All set? I'll launch it. Missing something? I'll walk you through each piece, about 5 minutes each.** Do you want WhatsApp, Slack, or both?

If the Mac isn't linked at all (check 1 ❌), lead with the Claude app step: nothing else can be checked until it's done.

### C. Walk through each missing piece
Use the step library (D). One step per message, wait, verify, next. When a piece turns ✅, say so in one line and move on.

### D. Step library
Send these **one numbered step at a time**.

**Claude desktop app** (verify: get_device_info succeeds)
1. Download Claude for Mac from https://claude.ai/download and open it.
2. Sign in with this same Claude account.
3. Open this chat in the desktop app, then say "done". *(This links the chat to their Mac.)*
4. Later, for daily runs: add Claude to System Settings → General → Login Items.

**WhatsApp desktop app** (verify: check A2)
1. Open the Mac App Store, search "WhatsApp Messenger" and install it.
2. Open WhatsApp on the Mac. It shows a QR code.
3. On your phone: WhatsApp → Settings → Linked devices → Link a device, then scan the code.
4. Leave the Mac app open for 10–20 minutes while it syncs. Say "done" when your groups show recent messages.
5. Add WhatsApp to System Settings → General → Login Items, so it stays synced. *(Explain: the digest only sees what the Mac app has synced.)*

**Claude in Chrome** (verify: check A3)
1. Ask: "Do you use more than one Chrome profile, e.g. work and personal?" If yes: "Switch to the one where your community Slacks are, or will be."
2. In that profile, open the Chrome Web Store, search "Claude" (by Anthropic), click Add to Chrome, and pin it.
3. Open the extension and sign in with this same Claude account.

**Slack communities in Chrome** (verify: check A4, and the workspace appears in S1)
1. In that Chrome profile, go to https://slack.com/signin and sign in with the email you use for the community.
2. Open the workspace. If Slack offers to open the desktop app, cancel and choose "use Slack in your browser".
3. Repeat for each community you want. Say "done".
4. When the extension asks for permission on app.slack.com, choose "always allow". *(Otherwise daily runs get stuck waiting for a click.)*

### E. Pick sources (once the pieces are ✅)
- **WhatsApp:** stage the DB, write the WhatsApp script, and run `python3 -I wa_extract.py --list-groups <staged path>`.
  Show the 40 most active groups as a numbered list. Ask: "Which ones? Reply with numbers."
  Store exact names, replacing trailing emoji with `%`.
- **Slack:** for each chosen workspace, open `https://app.slack.com/client/<team_id>` and run snippet S2.
  Show the channels as a numbered list. Ask which to track, suggesting 1–3 busy ones to start.
- **Projects (optional):** "Want me to flag things relevant to your work? Tell me your projects in a line each: what it is and who it sells to."

### F. Save and launch
1. Build the complete SKILL.md: this file, with CONFIG filled in and everything else unchanged. Save it with propose_skills
   (kind "improvement", target "community-digest"). Say: "Click Save on the card."
2. Run the first digest right away.
3. Offer a daily run in one line: "Want this every morning automatically? Tell me a time." If yes, create a scheduled task
   (on this computer, push notification on), with a prompt that runs this skill and, if the Mac isn't reachable, just notifies them to run
   /community-digest. Then tell them: at that time the Mac must be awake, with Claude, WhatsApp and Chrome open (Login Items). Offer the
   wake command if their Mac sleeps: `sudo pmset repeat wakeorpoweron MTWRFSU HH:MM:00`.

### Snippets
**S1: list logged-in Slack workspaces** (names and IDs only, never tokens)
```js
await new Promise(r => setTimeout(r, 5000));
Object.values(JSON.parse(localStorage.localConfig_v2 || '{"teams":{}}').teams).map(t => ({ id: t.id, name: t.name }))
```
**S2: list channels in a workspace** (set TEAM_ID)
```js
const t = Object.values(JSON.parse(localStorage.localConfig_v2).teams).find(x => x.id === 'TEAM_ID');
const call = async (m, p) => { const fd = new FormData(); fd.append('token', t.token); for (const k in p) fd.append(k, p[k]); return fetch('/api/' + m, { method: 'POST', body: fd, credentials: 'include' }).then(r => r.json()); };
const r = await call('users.conversations', { types: 'public_channel,private_channel', exclude_archived: 'true', limit: '200' });
(r.channels || []).map(c => ({ id: c.id, name: c.name, members: c.num_members })).sort((a, b) => b.members - a.members).slice(0, 40)
```

### Troubleshooting
| Symptom | Likely cause | What to tell them |
|---|---|---|
| WhatsApp folder missing | App not installed, or never opened | WhatsApp steps 1–4 |
| DB older than ~12h | App not opened recently | "Open WhatsApp on your Mac, wait a minute, then say done." |
| A group isn't in the list | Not in the top 40, or the name changed | Ask for the exact name and match it with `%` |
| Workspace missing in S1 | Logged in only in the Slack desktop app, or in another Chrome profile | Slack steps 1–2, in the right profile |
| Tab opens the wrong Slack account | Extension is in a different Chrome profile | Claude in Chrome step 1–2 in the right profile, then select that browser |
| "Permission prompt timed out" | Extension waiting for a click | "Check Chrome for a small Claude window and click Allow (pick always allow)." |
| Remote-device tools missing | Chat not open in the desktop app | Claude app step 3 |
| Scheduled run: "Mac not reachable" | Mac asleep, offline, or Claude closed | Login Items + the wake command |

## CONFIG — edit this block

```yaml
timezone: Asia/Kolkata          # used for timestamps in the digest
tz_offset_hours: 5.5            # same timezone as a number, for the WhatsApp script

whatsapp:
  # Exact group names as shown in WhatsApp. Use % for trailing emoji, e.g. "AI for GTM%".
  groups:
    - "Group name one"
    - "Group name two"

slack:
  # Chrome profile where these workspaces are logged in.
  # Get the deviceId by asking Claude to "list connected browsers".
  chrome_device_id: "PASTE-DEVICE-ID"
  workspaces:
    - team_id: "T0000000000"    # from https://app.slack.com/client/<TEAM_ID>/<CHANNEL_ID>
      channels: ["C0000000000"]

# Optional: what I'm working on, so relevant items get flagged.
my_projects: []
```

## Steps

1. **WhatsApp** (skip if `whatsapp.groups` is empty)
   - Request folder access (device_request_folder_access) to
     `~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared` if not already granted.
   - Stage `ChatStorage.sqlite` from that folder into the container (device_stage_files); wait a few seconds for it to land.
   - Check its last-modified time (from device_list_dir or the staging result). If it's older than ~12 hours, put a line at the
     top of the digest: "WhatsApp hasn't synced since <time>. Open the WhatsApp app and re-run for the latest messages."
   - Write the WhatsApp script below to the scratchpad and run:
     `DIGEST_TZ_OFFSET=<tz_offset_hours> python3 -I wa_extract.py <staged path> <hours> "<group 1>" "<group 2>" ...`
   - If the Mac isn't reachable, note "WhatsApp skipped: Mac not reachable" and continue.

2. **Slack** (skip if no workspaces)
   - Load the claude-in-chrome skill and tools; select_browser with `chrome_device_id`.
   - For each workspace: open a new tab at `https://app.slack.com/client/<team_id>/<first channel>`, wait ~6s.
   - Run the Slack script below via javascript_exec, with TEAM_ID, CHANNEL_IDS, HOURS and TZ filled in.
     It stores text in `window.__digest` and returns only counts. Never return tokens or raw text from javascript_exec.
   - To read the text: replace the page body with `<article><pre id="d"></pre></article>`, set its textContent to
     ~45k-character slices of `window.__digest`, and get_page_text each slice.
   - Close the tabs you opened.
   - If Chrome isn't connected, the workspace isn't logged in, or a permission prompt times out, note it and continue.

3. **Write the digest** in the format below. Deliver it in chat (or via SendUserMessage in a scheduled run).
   End with one line: messages read per source, and anything skipped and why.

## Digest format

Plain, direct, no hype. Most messages are noise; only include items that carry information.
Group by theme across all sources, never per group. Put the source in brackets at the end of each line, e.g. (WA: <group name>) or (Slack: <workspace>).
Flag one-person claims as claims, and flag vendor self-promotion.

**1. Experiments & results**
What someone actually tried, and what happened. Include numbers when given (reply rates, meetings booked, bounce rates, volume).
Format: *What they did* → *result* (who, source). Skip "I'm thinking of trying X" unless it got useful replies.

**2. Questions people are asking**
GTM engineering questions: outbound, deliverability, data and enrichment, tooling, infra and setup, calling, LinkedIn.
Sub-group by theme. For each: the question in one line → the best answer given, or "unanswered".
Unanswered questions are worth keeping; they show gaps and content ideas.

**3. Tools mentioned**
New or notable tools: name — what it's for — context (recommended / warned against / asked about), and how many people mentioned it.
Mark self-promotion. Skip household names unless something new was said about them.

**4. Relevant to my projects**
Only if `my_projects` is filled in: items from above that touch a project, with one line on why. Otherwise omit this section.

**Heads-up** (only if needed): security incidents, breaches, ban waves, blacklist changes. One line each.

**Skipped:** one line listing what was ignored (banter, self-promo, off-topic threads).

## WhatsApp script (wa_extract.py)

```python
{{WA_SCRIPT}}
```

If a WhatsApp update changes the schema, inspect `ZWACHATSESSION` / `ZWAMESSAGE` with `pragma table_info` and adapt.

## Slack script (run in the app.slack.com tab)

```js
{{SLACK_SCRIPT}}
```

## Requirements at run time
- Claude desktop app open on the Mac (so the session can reach it).
- WhatsApp desktop app installed and recently synced.
- Chrome open on the profile where the Slack workspaces are logged in, with the Claude extension connected and app.slack.com allowed.

Read-only: never send, post or react in any group or channel.
