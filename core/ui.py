"""Theme and small HTML helpers (same look as the trading dashboard, written separately)."""
import html as _h

import streamlit as st

BG, CARD, EDGE = "#0B1020", "#121A2F", "#1F2A44"
GOOD, BAD, WARN, ACCENT, MUTED = "#19D3A2", "#FF5C6C", "#FFB020", "#6C8CFF", "#8A97B5"
STATUS_COLOR = {"New": MUTED, "Shortlisted": ACCENT, "Applied": WARN, "Acknowledged": "#E07B39",
                "Interview": GOOD, "Offer": "#1F9E6B", "Rejected": BAD, "Skip": "#5B6783"}

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {{ font-family: 'Inter', system-ui, sans-serif; }}
.stApp {{ background: radial-gradient(1200px 600px at 10% -10%, #162044 0%, {BG} 55%) fixed; }}
.block-container {{ padding-top: 4rem; padding-bottom: 3rem; max-width: 1200px; }}
#MainMenu, footer {{ visibility: hidden; }}
.kpi {{ background:{CARD}; border:1px solid {EDGE}; border-radius:16px; padding:14px 16px; height:100%; }}
.kpi-l {{ color:{MUTED}; font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; font-weight:600; }}
.kpi-v {{ color:#fff; font-size:1.8rem; font-weight:800; letter-spacing:-0.02em; margin-top:4px; line-height:1.1; }}
.card {{ background:{CARD}; border:1px solid {EDGE}; border-radius:16px; padding:16px 18px; margin-bottom:12px; }}
.card h4 {{ margin:0 0 8px 0; color:#fff; font-size:1rem; font-weight:700; }}
.muted {{ color:{MUTED}; }}
.sub {{ color:{MUTED}; font-size:.82rem; }}
.badge {{ display:inline-block; padding:3px 10px; border-radius:999px; font-size:.74rem; font-weight:700; color:#fff; white-space:nowrap; }}
.barrow {{ display:flex; align-items:center; gap:10px; margin:6px 0; font-size:.88rem; }}
.barrow .l {{ width:110px; color:#fff; }} .barrow .n {{ width:30px; text-align:right; color:{MUTED}; }}
.bar {{ flex:1; background:#1A2440; border-radius:999px; height:9px; overflow:hidden; }}
.bar > div {{ height:100%; border-radius:999px; }}
.row {{ display:flex; gap:12px; align-items:flex-start; justify-content:space-between; padding:10px 0; border-bottom:1px solid {EDGE}; font-size:.92rem; }}
.row:last-child {{ border-bottom:none; }}
div[data-testid="stDataFrame"] {{ border:1px solid {EDGE}; border-radius:14px; overflow:hidden; }}
@media (max-width: 640px) {{ .kpi-v {{ font-size:1.4rem; }} .row {{ flex-direction:column; gap:4px; }} }}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def esc(x):
    return _h.escape("" if x is None else str(x))


def md(s):
    st.markdown(s, unsafe_allow_html=True)


def kpi(label, value):
    return f'<div class="kpi"><div class="kpi-l">{esc(label)}</div><div class="kpi-v">{esc(value)}</div></div>'


def badge(status):
    return f'<span class="badge" style="background:{STATUS_COLOR.get(status, MUTED)}">{esc(status)}</span>'


def card(inner, title=None):
    head = f"<h4>{esc(title)}</h4>" if title else ""
    return f'<div class="card">{head}{inner}</div>'
