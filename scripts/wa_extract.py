#!/usr/bin/env python3
"""
Read-only extract of recent messages from selected WhatsApp groups,
using the official WhatsApp Mac app's local database.

Usage:
  python3 wa_extract.py <path-to-ChatStorage.sqlite> <hours> "Group A" "Group B%" ...

Group names are matched with SQL LIKE, so use % for trailing emoji or
variable suffixes (e.g. "AI for GTM%").

Default DB location on macOS:
  ~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite

The script copies the DB to a temp folder first, so the live app file is
never opened or locked.
"""
import os
import shutil
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta, timezone

DEFAULT_DB = os.path.expanduser(
    "~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite"
)
APPLE_EPOCH = 978307200  # seconds between 1970-01-01 and 2001-01-01
TZ = timezone(timedelta(hours=float(os.environ.get("DIGEST_TZ_OFFSET", "5.5"))))
TYPES = {1: "[image]", 2: "[video]", 3: "[voice note]", 8: "[document]", 15: "[sticker]"}
SKIP_TYPES = (6, 10, 14)  # group events / system messages


def main():
    db = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DB
    hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    groups = sys.argv[3:]
    if not groups:
        sys.exit("Pass at least one group name after <db> <hours>.")

    tmp = tempfile.mkdtemp()
    try:
        for suffix in ("", "-wal", "-shm"):
            if os.path.exists(db + suffix):
                shutil.copy(db + suffix, os.path.join(tmp, "db.sqlite" + suffix))
        conn = sqlite3.connect(os.path.join(tmp, "db.sqlite"))
        since = datetime.now(timezone.utc).timestamp() - APPLE_EPOCH - hours * 3600

        for pattern in groups:
            rows = conn.execute(
                f"""
                select s.ZPARTNERNAME, m.ZMESSAGEDATE, m.ZISFROMME,
                       coalesce(nullif(g.ZCONTACTNAME, ''),
                                (select nullif(p.ZPUSHNAME, '') from ZWAPROFILEPUSHNAME p
                                  where p.ZJID = g.ZMEMBERJID limit 1),
                                nullif(g.ZFIRSTNAME, ''), '?'),
                       m.ZTEXT, m.ZMESSAGETYPE
                from ZWAMESSAGE m
                join ZWACHATSESSION s on s.Z_PK = m.ZCHATSESSION
                left join ZWAGROUPMEMBER g on g.Z_PK = m.ZGROUPMEMBER
                where s.ZSESSIONTYPE = 1
                  and s.ZPARTNERNAME like ?
                  and m.ZMESSAGEDATE > ?
                  and m.ZMESSAGETYPE not in {SKIP_TYPES}
                order by m.ZMESSAGEDATE
                """,
                (pattern, since),
            ).fetchall()
            if not rows:
                print(f"\n===== {pattern}: no messages =====")
                continue
            print(f"\n===== {rows[0][0]} ({len(rows)} msgs) =====")
            for _name, ts, from_me, sender, text, mtype in rows:
                t = datetime.fromtimestamp(ts + APPLE_EPOCH, TZ).strftime("%d %b %H:%M")
                body = (text or "").strip() or TYPES.get(mtype, f"[type {mtype}]")
                print(f"[{t}] {'Me' if from_me else sender}: {body}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def list_groups(db=DEFAULT_DB, limit=40):
    """Helper: print your most recently active groups, to find exact names."""
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    for (name,) in conn.execute(
        "select ZPARTNERNAME from ZWACHATSESSION where ZSESSIONTYPE = 1 "
        "and ZCONTACTJID like '%@g.us' order by ZLASTMESSAGEDATE desc limit ?",
        (limit,),
    ):
        print(name)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list-groups":
        list_groups(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DB)
    else:
        main()
