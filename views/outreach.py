"""Outreach: who has been contacted on LinkedIn and what happened."""
import pandas as pd
import streamlit as st


def render(db):
    out = db["outreach"]
    if not out:
        st.info("No outreach yet.")
        return
    df = pd.DataFrame(out)
    sent = df[df.status.isin(["Sent", "Accepted", "CV sent", "Replied"])]
    st.caption(f"{len(sent)} contacts reached, {len(df) - len(sent)} skipped or drafted. Message text is not stored here.")
    st.dataframe(df[["person", "company", "their_role", "type", "for", "status", "date", "next_date"]],
                 width="stretch", hide_index=True,
                 column_config={"person": "Person", "company": "Company", "their_role": "Their role", "type": "Type",
                                "for": "For application", "status": "Status", "date": "Date", "next_date": "Check again"})
