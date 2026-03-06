"""Simple password authentication for Streamlit."""

import json
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

# Session expires after 10 minutes of inactivity
INACTIVITY_TIMEOUT = 600

FEEDBACK_DIR = Path("feedback")
SESSION_LOG = FEEDBACK_DIR / "sessions.jsonl"


def _log_session():
    """Log session start."""
    FEEDBACK_DIR.mkdir(exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": "login",
    }
    with open(SESSION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def check_password() -> bool:
    """Show password input and return True if correct."""
    if st.session_state.get("authenticated"):
        last = st.session_state.get("last_activity", 0)
        if time.time() - last > INACTIVITY_TIMEOUT:
            st.session_state["authenticated"] = False
            st.warning("⏱️ Sessionen har gått ut på grund av inaktivitet. Logga in igen.")
        else:
            st.session_state["last_activity"] = time.time()
            return True

    try:
        password = st.secrets["app_password"]
    except (KeyError, FileNotFoundError):
        password = "klimatbudget2026"  # noqa: S105

    st.markdown("## 🔐 Logga in")
    st.markdown("Ange lösenord för att komma åt appen.")

    with st.form("login_form"):
        entered = st.text_input("Lösenord", type="password", key="password_input")
        submitted = st.form_submit_button("Logga in")

    if submitted:
        if entered == password:
            st.session_state["authenticated"] = True
            st.session_state["last_activity"] = time.time()
            _log_session()
            st.switch_page("app.py")
        else:
            st.error("Fel lösenord. Försök igen.")

    return False
