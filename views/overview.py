"""Overview: the numbers, the funnel, applications sent, what needs attention."""
import streamlit as st

from core import data as D
from core import ui


def render(db):
    apps, outreach = db["applications"], db["outreach"]
    c = D.counts(apps)
    sent = [a for a in apps if a["status"] in D.SENT]
    due = D.due(apps)
    tiles = [("Roles tracked", len(apps)), ("Applications sent", len(sent)),
             ("Waiting for reply", c["Applied"] + c["Acknowledged"]), ("Interviews", c["Interview"]),
             ("Offers", c["Offer"]), ("Rejected", c["Rejected"]), ("Follow-up due", len(due)),
             ("Outreach sent", sum(1 for o in outreach if o["status"] in ("Sent", "Accepted", "CV sent", "Replied")))]
    cols = st.columns(4)
    for i, (label, value) in enumerate(tiles):
        with cols[i % 4]:
            ui.md(ui.kpi(label, value))
            st.write("")

    left, right = st.columns([3, 2])
    with left:
        rows = "".join(
            f'<div class="row"><div><b>{ui.esc(a["company"])}</b><br><span class="sub">{ui.esc(a["role"])}</span></div>'
            f'<div style="text-align:right">{ui.badge(a["status"])}<br><span class="sub">applied {ui.esc(a["applied"] or "n/a")}</span></div></div>'
            for a in sorted(sent, key=lambda a: a["applied"], reverse=True)) or '<div class="muted">No applications sent yet.</div>'
        ui.md(ui.card(rows, "Applications sent"))
    with right:
        top = max(c.values()) or 1
        bars = "".join(
            f'<div class="barrow"><span class="l">{s}</span><div class="bar"><div style="width:{c[s] / top * 100:.0f}%;background:{ui.STATUS_COLOR[s]}"></div></div><span class="n">{c[s]}</span></div>'
            for s in D.ORDER)
        ui.md(ui.card(bars, "Pipeline by status"))
        if due:
            items = "".join(f'<div class="row"><div><b>{ui.esc(a["company"])}</b><br><span class="sub">{ui.esc(a["role"])}</span></div>'
                            f'<div class="sub">{ui.esc(a["next_action"])}</div></div>' for a in due)
        else:
            items = '<div class="muted">Nothing due today.</div>'
        ui.md(ui.card(items, "Needs attention"))
