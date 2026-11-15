"""Applications: every tracked role with filters."""
import pandas as pd
import streamlit as st

from core import data as D


def render(db):
    apps = [a for a in db["applications"] if a["status"] != "Skip"]
    if not apps:
        st.info("No applications or shortlisted roles yet.")
        return
    df = pd.DataFrame(apps)
    c1, c2 = st.columns(2)
    status = c1.multiselect("Status", [s for s in D.ORDER if s != "Skip"], default=[s for s in D.ORDER if s != "Skip" and s in set(df.status)])
    track = c2.multiselect("Track", sorted(set(df.track) - {""}), default=sorted(set(df.track) - {""}))
    view = df[df.status.isin(status) & df.track.isin(track)]
    st.dataframe(
        view[["company", "role", "track", "fit", "status", "applied", "updated", "next_action", "next_date", "url"]],
        width="stretch", hide_index=True,
        column_config={"url": st.column_config.LinkColumn("Posting", display_text="open"),
                       "company": "Company", "role": "Role", "track": "Track", "fit": "Fit",
                       "status": "Status", "applied": "Applied", "updated": "Updated",
                       "next_action": "Next action", "next_date": "Due"})
