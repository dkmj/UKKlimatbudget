"""Simple password authentication for Streamlit."""

import json
from datetime import datetime
from pathlib import Path

import streamlit as st

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
        return True

    try:
        password = st.secrets["app_password"]
    except (KeyError, FileNotFoundError):
        password = "klimatbudget2026"  # noqa: S105

    st.markdown("## 🔐 Logga in")
    st.markdown("Ange lösenord för att komma åt appen.")

    entered = st.text_input("Lösenord", type="password", key="password_input")

    if st.button("Logga in", key="login_button"):
        if entered == password:
            st.session_state["authenticated"] = True
            _log_session()
            st.rerun()
        else:
            st.error("Fel lösenord. Försök igen.")

    return False
