"""Daily request limiter for Gemini API calls.

Uses a simple JSON file to track requests per UTC date.
Resets automatically each new day.
"""

import json
from datetime import UTC, datetime
from pathlib import Path

RATE_FILE = Path("feedback/daily_requests.json")
DAILY_LIMIT = 1400


def _load() -> dict:
    """Load the current rate-limit state."""
    if RATE_FILE.exists():
        with open(RATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"date": "", "count": 0}


def _save(state: dict):
    """Persist rate-limit state."""
    RATE_FILE.parent.mkdir(exist_ok=True)
    with open(RATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)


def check_rate_limit() -> tuple[bool, int, int]:
    """Check if requests are still allowed today.

    Returns (allowed, count, limit).
    """
    today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
    state = _load()

    # Reset counter on new day
    if state["date"] != today:
        state = {"date": today, "count": 0}
        _save(state)

    return state["count"] < DAILY_LIMIT, state["count"], DAILY_LIMIT


def increment_request():
    """Record one API request."""
    today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
    state = _load()

    if state["date"] != today:
        state = {"date": today, "count": 0}

    state["count"] += 1
    _save(state)
