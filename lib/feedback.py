# -*- coding: utf-8 -*-
"""Feedback collection with thumbs up/down."""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path

FEEDBACK_DIR = Path("feedback")
FEEDBACK_FILE = FEEDBACK_DIR / "feedback.jsonl"


def _save_feedback(component: str, context: str, rating: str):
    """Save a feedback entry."""
    FEEDBACK_DIR.mkdir(exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "component": component,
        "context": context,
        "rating": rating,
    }
    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def thumbs_feedback(component: str, context: str = "", key_suffix: str = ""):
    """Render thumbs up/down buttons and save feedback."""
    key = f"fb_{component}_{key_suffix}"

    if key in st.session_state and st.session_state[key] is not None:
        st.caption(f"Tack för din feedback! ({'👍' if st.session_state[key] == 'up' else '👎'})")
        return

    cols = st.columns([1, 1, 8])
    with cols[0]:
        if st.button("👍", key=f"{key}_up", help="Bra!"):
            _save_feedback(component, context, "up")
            st.session_state[key] = "up"
            st.rerun()
    with cols[1]:
        if st.button("👎", key=f"{key}_down", help="Kan förbättras"):
            _save_feedback(component, context, "down")
            st.session_state[key] = "down"
            st.rerun()


def load_feedback() -> list[dict]:
    """Load all feedback entries."""
    if not FEEDBACK_FILE.exists():
        return []
    entries = []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries
