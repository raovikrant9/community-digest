# Community Digest

Wake up every morning with 500+ notifications across multiple groups? And have trouble picking nuggets of information from there? This repo helps collate information from whatsapp and slack groups into a digest to make content more consumable.

Each day it gives you:

1. **Experiments & results**: what people actually tried, and the numbers they saw
2. **Questions people are asking**: grouped by theme, with the best answer given (or "unanswered")
3. **Tools mentioned**: what's new, what it's for, who recommended or warned against it

Optionally, it also flags anything relevant to projects you list.

It runs from the Claude desktop app on a Mac, on demand (`/community-digest`) or on a daily schedule.

> **Before you start**
> - **Mac only.** WhatsApp is read from the WhatsApp **Mac app's** local database. WhatsApp Web doesn't work.
> - **Open WhatsApp regularly.** The digest only sees what the desktop app has synced. Add WhatsApp to your Login Items so it's always running.
> - **Slack needs Chrome.** Your community workspaces must be logged in at app.slack.com in a Chrome profile with the Claude in Chrome extension. Using only the Slack desktop app isn't enough.
> - **Read-only, but not official.** Nothing is ever posted or sent. The WhatsApp database format is undocumented and can change. Slack is read through your own browser session, which is a grey area in Slack's terms.
> - **Other people's messages go to an AI.** Keep digests to yourself.

---

## How it works

| Source | How messages are read | Why this way |
|---|---|---|
| **WhatsApp** | Reads a *copy* of the local database of the official WhatsApp Mac app | No unofficial client or bot, so WhatsApp sees nothing unusual. No ban risk beyond normal use. |
| **Slack** | Uses your logged-in Slack tab in Chrome (via the Claude in Chrome extension) to call Slack's own web API | No Slack app install or admin approval needed. Works for community workspaces where you're just a member. |

Claude then filters and summarises the text into the digest format defined in `skill/SKILL.md`.

Everything is **read-only**. Nothing is ever posted, sent or reacted to.

### What it can't see
- Images, voice notes and attached documents (they show up as placeholders).
- WhatsApp messages the desktop app hasn't synced yet.
- Slack workspaces you're not logged into in the chosen Chrome profile.

---

## Requirements

- A **Mac** with the **official WhatsApp desktop app** (from the Mac App Store) logged in. WhatsApp Web in a browser doesn't work for this.
- The **Claude desktop app**, signed in to a plan that includes Claude's agent features (scheduled tasks, skills, connecting to your computer).
- **Google Chrome** with the **Claude in Chrome** extension, for Slack.
- Your Slack community workspaces logged in on the **web** (`app.slack.com`) in that Chrome profile.

---

## Setup

You don't need to read a guide. Claude walks you through it.

1. Copy everything in [`skill/SKILL.md`](skill/SKILL.md).
2. Open the **Claude desktop app** on your Mac (download it from https://claude.ai/download), paste the file into a chat, and say **"Save this as a skill called community-digest."** Click **Save** on the card.
3. Type **`/community-digest`**.

Claude checks what's already set up on your Mac and shows you a checklist (Claude app, WhatsApp desktop app, Claude in Chrome, Slack in Chrome). If something is missing, it guides you through that piece one step at a time. Then it helps you pick your groups and channels and runs your first digest. It can also set up a daily run.

## Customising

- **Add or remove WhatsApp groups:** edit `whatsapp.groups` in the skill's CONFIG. Use `%` for trailing emoji (`"AI for GTM%"`).
- **Add Slack channels:** add channel IDs to a workspace's `channels`, or add another workspace entry.
- **Change the digest:** edit the "Digest format" section of the skill. It's plain English.
- **Flag things for your projects:** list them under `my_projects`, e.g. `"OttoSales: voice AI for field sales, selling to industrial B2B"`.

## Running the scripts yourself

```bash
# WhatsApp: list group names
python3 scripts/wa_extract.py --list-groups

# WhatsApp: last 24h from two groups (copies the DB first, never touches the live file)
python3 scripts/wa_extract.py ~/Library/Group\ Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite 24 "Group one" "Group two%"
```
Your Terminal needs **Full Disk Access** (System Settings → Privacy & Security) to read that folder.

`scripts/slack_pull.js` can be pasted into the DevTools console of a logged-in `app.slack.com` tab after filling in `TEAM_ID` and `CHANNEL_IDS`. The text ends up in `window.__digest`.

If you edit either script, run `python3 scripts/build_skill.py` to rebuild `skill/SKILL.md` from `skill/SKILL.template.md`.

---

## Keeping your config private (if you fork this repo)

Your filled-in skill contains your group names, Slack IDs and projects. Don't commit it.
- Save personal copies as `*.local.md` (for example `skill/SKILL.local.md`). The `.gitignore` already excludes them, along with chat exports, digests and database copies.
- Turn on the safety check, which blocks commits containing real Slack or Chrome IDs:
  ```bash
  git config core.hooksPath .githooks
  ```

## Privacy and risk notes

- You're feeding other people's messages to an LLM. Keep the digest for yourself, and don't repost it with names attached.
- **WhatsApp:** this only reads your own Mac's database, so there's no automation on your account. The database format isn't documented and can change after WhatsApp updates; the skill tells Claude to adapt if it does.
- **Slack:** reading through your own session is low risk for your account, but sits in a grey area of Slack's terms. It's read-only and low-volume. Don't use it to bulk-export workspaces.
- Slack tokens never leave the browser tab; the script returns only counts and cleaned text.

## License
MIT
