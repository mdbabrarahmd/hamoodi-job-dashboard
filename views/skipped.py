"""Skipped roles and why."""
import pandas as pd
import streamlit as st


def render(db):
    skipped = [a for a in db["applications"] if a["status"] == "Skip"]
    if not skipped:
        st.info("Nothing skipped yet.")
        return
    df = pd.DataFrame(skipped)
    st.caption(f"{len(df)} roles read and skipped. Each reason is the main mismatch found when the posting was read.")
    st.dataframe(df[["company", "role", "track", "fit", "why", "url"]], width="stretch", hide_index=True,
                 column_config={"url": st.column_config.LinkColumn("Posting", display_text="open"), "company": "Company",
                                "role": "Role", "track": "Track", "fit": "Fit", "why": "Why skipped"})
