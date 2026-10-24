// Slack pull — run inside a logged-in https://app.slack.com tab
// (e.g. via Claude in Chrome's javascript tool, or paste into DevTools console).
//
// It reuses your existing browser session to call Slack's own web API,
// so no app install or admin approval is needed. Read-only.
//
// Set TEAM_ID / CHANNEL_IDS from your channel URLs:
//   https://app.slack.com/client/<TEAM_ID>/<CHANNEL_ID>
//
// Result is stored in window.__digest (text) and the call returns only counts,
// so tokens and raw text never leave the page unless you read them deliberately.

const TEAM_ID = 'T0000000000';
const CHANNEL_IDS = ['C0000000000'];
const HOURS = 24;
const TZ = 'Asia/Kolkata';

const cfg = JSON.parse(localStorage.localConfig_v2);
const team = Object.values(cfg.teams).find((x) => x.id === TEAM_ID);
if (!team) throw new Error('Workspace not logged in on this browser profile: ' + TEAM_ID);

const call = async (method, params) => {
  const fd = new FormData();
  fd.append('token', team.token);
  for (const k in params) fd.append(k, params[k]);
  return fetch('/api/' + method, { method: 'POST', body: fd, credentials: 'include' }).then((r) => r.json());
};

const names = {};
const nameOf = async (u) => {
  if (!u) return '?';
  if (names[u]) return names[u];
  const r = await call('users.info', { user: u });
  names[u] = r.ok ? r.user.profile.display_name || r.user.real_name || r.user.name : u;
  return names[u];
};
const clean = (s) =>
  (s || '')
    .replace(/<(https?:\/\/[^>|?#]+)[^>|]*(\|([^>]*))?>/g, (x, url, _, label) => (label ? `${label} (${url})` : url))
    .replace(/<@(\w+)>/g, '@$1');
const fmt = (ts) =>
  new Date(ts * 1000).toLocaleString('en-GB', { timeZone: TZ, day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });

const oldest = String(Date.now() / 1000 - HOURS * 3600);
const sections = [];
const counts = {};

for (const ch of CHANNEL_IDS) {
  const info = await call('conversations.info', { channel: ch });
  let msgs = [];
  let cursor = '';
  for (let page = 0; page < 20; page++) {
    const h = await call('conversations.history', { channel: ch, oldest, limit: '200', cursor });
    if (!h.ok) throw new Error(`conversations.history failed for ${ch}: ${h.error}`);
    msgs = msgs.concat(h.messages || []);
    cursor = h.response_metadata && h.response_metadata.next_cursor;
    if (!h.has_more || !cursor) break;
  }
  const lines = [];
  for (const m of msgs.slice().reverse()) {
    if (m.subtype && !['thread_broadcast', 'bot_message'].includes(m.subtype)) continue;
    lines.push(`[${fmt(m.ts)}] ${await nameOf(m.user)}: ${clean(m.text) || '[attachment]'}`);
    if (m.reply_count) {
      const rr = await call('conversations.replies', { channel: ch, ts: m.ts, limit: '200' });
      for (const r of (rr.messages || []).slice(1)) {
        lines.push(`    ↳ [${fmt(r.ts)}] ${await nameOf(r.user)}: ${clean(r.text) || '[attachment]'}`);
      }
    }
  }
  const chName = info.ok ? info.channel.name : ch;
  counts[chName] = { posts: msgs.length, lines: lines.length };
  sections.push(`===== ${team.name} #${chName} =====\n` + lines.join('\n'));
}

let out = sections.join('\n\n');
for (const id in names) out = out.split('@' + id).join('@' + names[id]);
// Strip query strings/ids so the text can be read through tools that block URL parameters.
window.__digest = out
  .replace(/\n\s*\n/g, '\n')
  .replace(/https?:\/\/([^\/\s)>|]+)\S*/g, '[link:$1]')
  .replace(/[=&;]/g, ' ')
  .replace(/\b[A-Za-z0-9_-]{30,}\b/g, '[id]');

({ team: team.name, counts, chars: window.__digest.length });
