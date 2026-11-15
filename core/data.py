"""Load the job snapshot and compute the numbers the pages show.

On Streamlit Cloud the snapshot comes from the app's Secrets (JOBS_JSON), never from the public repo.
On the owner's Mac it falls back to data/jobs.json, which is git-ignored and not uploaded.
"""
import json
from datetime import date
from pathlib import Path

import streamlit as st

LOCAL = Path(__file__).resolve().parent.parent / "data" / "jobs.json"
SENT = ["Applied", "Acknowledged", "Interview", "Offer", "Rejected"]
ORDER = ["New", "Shortlisted", "Applied", "Acknowledged", "Interview", "Offer", "Rejected", "Skip"]
EMPTY = {"updated": "", "applications": [], "outreach": []}


@st.cache_data(ttl=60)
def load():
    try:
        raw = st.secrets.get("JOBS_JSON", "")
    except Exception:
        raw = ""
    if raw:
        return json.loads(raw)
    if LOCAL.exists():
        return json.loads(LOCAL.read_text(encoding="utf-8"))
    return EMPTY


def counts(apps):
    c = {s: 0 for s in ORDER}
    for a in apps:
        c[a["status"]] = c.get(a["status"], 0) + 1
    return c


def due(apps):
    """Applied or Acknowledged roles whose next-action date has arrived."""
    today = date.today().isoformat()
    return [a for a in apps if a["status"] in ("Applied", "Acknowledged") and a["next_date"] and a["next_date"] <= today]
