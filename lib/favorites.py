"""Star/favorite system for klimatåtgärder."""

from pathlib import Path

import streamlit as st

MAX_FAVORITES = 10

# ---------------------------------------------------------------------------
# Linkroll — external resources shown at the bottom of the sidebar.
# Add new entries here as {label, url, emoji} dicts.
# All links open in a new tab.
# ---------------------------------------------------------------------------
LINKS = [
    {
        "label": "Klimatbudget — Uppsala kommun",
        "url": "https://www.uppsala.se/kommun-och-politik/kommunens-mal-och-budget/mal-och-budget/klimatbudget/",
    },
    {
        "label": "Deep Research — webbversion",
        "url": "https://gemini.google.com/share/e6409eaadff7",
    },
]

# Deep-research report (kept as constants for the Rapport page).
REPORT_WEB_URL = "https://gemini.google.com/share/e6409eaadff7"
REPORT_PDF_PATH = Path("assets/generated/deep_research_rapport.pdf")


# ---------------------------------------------------------------------------
# Favorites helpers
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Sidebar rendering
# ---------------------------------------------------------------------------
def _render_sidebar_linkroll():
    """Render linkroll styled to match the sidebar navigation items."""
    with st.sidebar:
        st.markdown("---")
        # Build link items that visually match the Streamlit nav entries
        link_items = "".join(
            f'<a href="{link["url"]}" target="_blank" rel="noopener">'
            f"{link['label']}</a>"
            for link in LINKS
        )
        st.markdown(
            f"""
            <div class="sidebar-linkroll">
                <p class="linkroll-heading">Länkar</p>
                {link_items}
            </div>
            """,
            unsafe_allow_html=True,
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
                    if st.button(
                        "✕",
                        key=f"sidebar_unfav_{f['nr']}",
                        help="Ta bort favorit",
                    ):
                        remove_favorite(f["nr"])
                        st.rerun()

    # Linkroll (always shown)
    _render_sidebar_linkroll()
