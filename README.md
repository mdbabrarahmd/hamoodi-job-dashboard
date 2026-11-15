# Job search dashboard

A small Streamlit dashboard for tracking a job search: applications, status, follow-ups and outreach.

This repository contains code only. The data is never stored here: it is read at run time from the app's Secrets (`JOBS_JSON`), and the app shows nothing until the visitor enters the passcode kept in the same Secrets (`APP_PASSCODE`). With no passcode configured it fails closed.

- `app.py` shell and navigation, `core/gate.py` passcode, `core/data.py` data loader, `core/ui.py` theme, `views/` the pages.
- Run locally: `streamlit run app.py` (reads `data/jobs.json` if present; that file is git-ignored).
