"""Passcode gate. The app shows nothing until the visitor enters the passcode kept in the app's Secrets.

Fails closed: on Streamlit Cloud with no APP_PASSCODE secret set, the app refuses to show anything.
The only open mode is on the owner's Mac, where data/jobs.json exists locally and no passcode is set
(that file is never uploaded to GitHub).
"""
import hmac
import time

import streamlit as st

MAX_TRIES = 5


def _secret(name):
    try:
        return str(st.secrets.get(name, "") or "").strip()
    except Exception:
        return ""


def passed():
    if st.session_state.get("authed"):
        return True
    wanted = _secret("APP_PASSCODE")
    if not wanted:
        from core import data as D
        if D.LOCAL.exists():                       # owner's Mac only
            st.session_state["authed"] = True
            return True
        st.markdown("### 🔒 Not set up yet")
        st.caption("No passcode has been set for this dashboard, so nothing is shown.")
        return False

    tries = st.session_state.get("tries", 0)
    st.markdown("### 🔒 Job search dashboard")
    if tries >= MAX_TRIES:
        st.error("Too many wrong attempts. Close this tab and open the link again.")
        return False
    with st.form("gate", clear_on_submit=True):
        given = st.text_input("Passcode", type="password")
        go = st.form_submit_button("Open")
    if go:
        if hmac.compare_digest(given.encode(), wanted.encode()):
            st.session_state["authed"] = True
            st.rerun()
        st.session_state["tries"] = tries + 1
        time.sleep(1.5)
        st.error("Wrong passcode.")
    return False
