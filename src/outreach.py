from __future__ import annotations
import os
from typing import Dict, Iterable, List
from .rate_limit import SendBudget, natural_delay, in_quiet_hours
from .utils import send_email, utcnow

def prepare_vars(row: Dict) -> Dict:
    return {
        "name": row.get("name") or row.get("handle") or "there",
        "niche": row.get("niche") or "",
        "recent_video": row.get("recent_video") or "",
        "value_prop": row.get("value_prop") or "",
        "sender_name": os.getenv("SENDER_NAME", "Your Name")
    }

def send_email_batch(batch: Iterable[Dict], dry_run: bool, log_rows: List[Dict]):
    smtp_host = os.getenv("EMAIL_SMTP_HOST"); smtp_port = os.getenv("EMAIL_SMTP_PORT", "587")
    smtp_user = os.getenv("EMAIL_SMTP_USER"); smtp_pass = os.getenv("EMAIL_SMTP_PASS")
    sender = os.getenv("EMAIL_FROM"); reply_to = os.getenv("EMAIL_REPLY_TO","")
    budget = SendBudget()

    for row in batch:
        status = "skipped"
        if in_quiet_hours() or not budget.allow():
            status = "paused_quiet_or_budget"
        else:
            ok = True if dry_run else send_email(
                smtp_host, int(smtp_port), smtp_user, smtp_pass,
                sender, reply_to, row.get("email"), row.get("subject"), row.get("body")
            )
            status = "sent" if ok else "failed"
            if not dry_run and ok:
                budget.mark(); natural_delay()

        log_rows.append({
            **row, "ts_utc": utcnow(), "status": status
        })

def manual_dm_checklist(batch: Iterable[Dict]) -> Iterable[Dict]:
    for row in batch:
        yield {
            "id": row.get("id"),
            "handle": row.get("handle"),
            "platform": "tiktok",
            "message": f"{row.get('subject','')}\n\n{row.get('body','')}",
            "note": "Send manually via TikTok; respect platform rules."
        }
