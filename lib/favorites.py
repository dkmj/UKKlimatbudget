# -*- coding: utf-8 -*-
"""Star/favorite system for klimatåtgärder."""

import streamlit as st

MAX_FAVORITES = 10


def get_favorites() -> list[dict]:
    """Get the current list of favorites from session state."""
    if "favorites" not in st.session_state:
        st.session_state.favorites = []
    return st.session_state.favorites


def is_favorite(nr: str) -> bool:
    """Check if an action is in the favorites list."""
    return any(f["nr"] == nr for f in get_favorites())


def add_favorite(nr: str, text: str, område: str) -> bool:
    """Add an action to favorites. Returns False if list is full."""
    favs = get_favorites()
    if len(favs) >= MAX_FAVORITES:
        return False
    if not is_favorite(nr):
        favs.append({"nr": nr, "text": text[:80], "område": område})
    return True


def remove_favorite(nr: str):
    """Remove an action from favorites."""
    st.session_state.favorites = [f for f in get_favorites() if f["nr"] != nr]


# Linkroll — external resources shown at the bottom of the sidebar.
# Add new entries here as {label, url, emoji} dicts.
LINKS = [
    {
        "label": "Klimatbudget — Uppsala kommun",
        "url": "https://www.uppsala.se/kommun-och-politik/kommunens-mal-och-budget/mal-och-budget/klimatbudget/",
        "emoji": "🌍",
    },
]


def _render_sidebar_linkroll():
    """Render a linkroll section at the bottom of the sidebar."""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🔗 Länkar")
        for link in LINKS:
            st.markdown(
                f"{link['emoji']} [{link['label']}]({link['url']})"
            )


def render_sidebar_favorites():
    """Render favorites and linkroll in the sidebar."""
    favs = get_favorites()

    with st.sidebar:
        # Favorites (only if any exist)
        if favs:
            st.markdown("---")
            st.markdown(f"### ⭐ Favoriter ({len(favs)}/{MAX_FAVORITES})")
            for f in favs:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.caption(f"**{f['nr']}** — {f['text']}")
                with col2:
                    if st.button("✕", key=f"sidebar_unfav_{f['nr']}", help="Ta bort favorit"):
                        remove_favorite(f["nr"])
                        st.rerun()

    # Linkroll (always shown)
    _render_sidebar_linkroll()
