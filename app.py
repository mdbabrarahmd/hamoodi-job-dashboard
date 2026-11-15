"""Job search dashboard: applications, status, follow-ups and outreach, behind a passcode.

Run:  streamlit run app.py
Data: the app's Secrets (JOBS_JSON) on Streamlit Cloud, or data/jobs.json on the owner's Mac (not in GitHub).
Passcode: APP_PASSCODE in the app's Secrets. Nothing is shown without it.
"""
import streamlit as st

st.set_page_config(page_title="Job Search", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

from core import gate             # noqa: E402
from core import ui               # noqa: E402

ui.inject_css()
if not gate.passed():
    st.stop()

from core import data as D        # noqa: E402
from views import applications, outreach, overview, skipped   # noqa: E402

DB = D.load()

ui.md('<div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px">'
      '<div style="font-weight:800;font-size:1.1rem;color:#fff">🎯 Job search <span class="muted" style="font-weight:500">· tracking since 11 Nov 2026</span></div>'
      f'<div class="sub">Updated {ui.esc(DB.get("updated") or "never")}</div></div>')


def page(mod):
    def run():
        mod.render(DB)
    return run


pg = st.navigation([
    st.Page(page(overview), title="Overview", icon=":material/dashboard:", url_path="overview", default=True),
    st.Page(page(applications), title="Applications", icon=":material/work:", url_path="applications"),
    st.Page(page(outreach), title="Outreach", icon=":material/groups:", url_path="outreach"),
    st.Page(page(skipped), title="Skipped", icon=":material/block:", url_path="skipped"),
], position="top")
pg.run()
