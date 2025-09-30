from __future__ import annotations
import argparse, os
from pathlib import Path
import pandas as pd

from .dedupe import dedupe_df
from .templating import render_template
from .outreach import prepare_vars, send_email_batch, manual_dm_checklist
from .utils import write_csv

def cmd_validate(args):
    df = pd.read_csv(args.infile)
    out = dedupe_df(df)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)
    print(f"[validate] wrote {args.out} ({len(out)} rows)")

def cmd_render(args):
    leads = pd.read_csv(args.infile).to_dict(orient="records")
    tpl = Path(args.template).read_text(encoding="utf-8")
    rows = []
    for r in leads:
        vars = prepare_vars(r)
        body = render_template(tpl, vars)
        rows.append({
            "id": r.get("id"),
            "email": r.get("email"),
            "handle": r.get("handle"),
            "subject": body.splitlines()[0].replace("Subject:", "").strip() if "Subject:" in body else "Collab idea",
            "body": body
        })
    write_csv(args.out, rows)
    print(f"[render] wrote {args.out} ({len(rows)} messages)")

def cmd_send(args):
    batch = pd.read_csv(args.batch).to_dict(orient="records")
    if args.channel == "email":
        logs = []
        send_email_batch(batch, args.dry_run, logs)
        Path("reports").mkdir(parents=True, exist_ok=True)
        write_csv("reports/sent.log.csv", logs)
        print(f"[send] appended {len(logs)} rows to reports/sent.log.csv")
    elif args.channel == "manual_dm":
        out = args.out or "out/dm_checklist.csv"
        rows = list(manual_dm_checklist(batch))
        write_csv(out, rows)
        print(f"[send] wrote {out} ({len(rows)} items)")

def cmd_followup(args):
    # Simple example: reuse any previously 'sent' rows as follow-up candidates.
    log = pd.read_csv(args.log)
    sent = log[log["status"] == "sent"].copy()
    out = args.out or "out/followup.batch.csv"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sent.to_csv(out, index=False)
    print(f"[followup] wrote {out} ({len(sent)} candidates)")

def cmd_update(args):
    df = pd.read_csv(args.infile)
    mask = (df["id"].astype(str) == str(args.id)) | (df.get("handle","").astype(str) == str(args.id))
    df.loc[mask, "status"] = args.status
    if args.notes: df.loc[mask, "notes"] = args.notes
    df.to_csv(args.infile, index=False)
    print(f"[update] updated {args.infile}")

def cmd_report(args):
    import datetime as dt
    log = pd.read_csv(args.log)
    total_sent = int((log["status"] == "sent").sum())
    total_failed = int((log["status"] == "failed").sum())
    summary = [{
        "period_ending_utc": dt.datetime.utcnow().isoformat(timespec="seconds"),
        "total_sent": total_sent,
        "total_failed": total_failed
    }]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    write_csv(args.out, summary)
    print(f"[report] wrote {args.out}")

def build():
    p = argparse.ArgumentParser(description="TikTok Shop Affiliate Outreach Bot (consent-based)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("validate", help="Validate & dedupe leads")
    s.add_argument("--in", dest="infile", required=True)
    s.add_argument("--out", default="data/leads.valid.csv")
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("render", help="Render messages from template")
    s.add_argument("--in", dest="infile", required=True)
    s.add_argument("--template", required=True)
    s.add_argument("--out", default="out/batch.csv")
    s.set_defaults(func=cmd_render)

    s = sub.add_parser("send", help="Send a batch (email) or produce manual DM checklist")
    s.add_argument("--batch", required=True)
    s.add_argument("--channel", choices=["email","manual_dm"], required=True)
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--out")
    s.set_defaults(func=cmd_send)

    s = sub.add_parser("followup", help="Prepare follow-up batch from sent log")
    s.add_argument("--log", default="reports/sent.log.csv")
    s.add_argument("--days-since", type=int, default=3)  # placeholder for future date logic
    s.add_argument("--template", required=True)          # unused here; plan for future
    s.add_argument("--out", default="out/followup.batch.csv")
    s.set_defaults(func=cmd_followup)

    s = sub.add_parser("update", help="Update a lead status")
    s.add_argument("--in", dest="infile", required=True)
    s.add_argument("--id", required=True)
    s.add_argument("--status", required=True)
    s.add_argument("--notes")
    s.set_defaults(func=cmd_update)

    s = sub.add_parser("report", help="Create summary from sent log")
    s.add_argument("--log", default="reports/sent.log.csv")
    s.add_argument("--out", default="reports/weekly_summary.csv")
    s.set_defaults(func=cmd_report)
    return p

def main():
    args = build().parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
