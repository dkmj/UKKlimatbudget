"""Shared navigation — compact icon bar for sub-pages and hub footer."""

import streamlit as st

# Page definitions: key, icon, label, path, accent_color
PAGE_DEFS = [
    {
        "key": "hub",
        "icon": "🌍",
        "label": "Klimatbudgeten",
        "path": "app.py",
        "accent": "#D4A843",
    },
    {
        "key": "oversikt",
        "icon": "📊",
        "label": "Översikt",
        "path": "pages/1_Översikt.py",
        "accent": "#7B2D8E",
    },
    {
        "key": "utforska",
        "icon": "🔍",
        "label": "Utforska",
        "path": "pages/2_Utforska.py",
        "accent": "#D94F7A",
    },
    {
        "key": "quiz",
        "icon": "❓",
        "label": "Quiz",
        "path": "pages/3_Quiz.py",
        "accent": "#D4A843",
    },
    {
        "key": "podcast",
        "icon": "🎙️",
        "label": "Podcast",
        "path": "pages/4_Podcast.py",
        "accent": "#8B9B58",
    },
    {
        "key": "presentation",
        "icon": "📑",
        "label": "Presentation",
        "path": "pages/5_Presentation.py",
        "accent": "#5B2D8E",
    },
    {
        "key": "chatt",
        "icon": "💬",
        "label": "Chatt",
        "path": "pages/6_Chatt.py",
        "accent": "#E8476C",
    },
    {
        "key": "rapport",
        "icon": "📄",
        "label": "Rapport",
        "path": "pages/7_Rapport.py",
        "accent": "#6B7D3A",
    },
    {
        "key": "flashcards",
        "icon": "🃏",
        "label": "Flashcards",
        "path": "pages/8_Flashcards.py",
        "accent": "#D4A843",
    },
]

# Sub-pages only (exclude the hub itself)
_SUB_PAGES = [p for p in PAGE_DEFS if p["key"] != "hub"]


def render_nav_bar(current_page: str):
    """Render a compact icon navigation bar at the top of sub-pages."""
    # Home link + sub-page icons
    items = [PAGE_DEFS[0]] + _SUB_PAGES  # hub first, then all sub-pages

    cols = st.columns(len(items))
    for col, page in zip(cols, items):
        with col:
            if page["key"] == current_page:
                # Active page — styled label, not clickable
                st.markdown(
                    f'<div class="nav-item active">'
                    f'{page["icon"]}<br>'
                    f'<span class="nav-label">{page["label"]}</span>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.page_link(
                    page["path"],
                    label=f'{page["icon"]} {page["label"]}',
                    use_container_width=True,
                )

    # Breadcrumb
    current_def = next((p for p in PAGE_DEFS if p["key"] == current_page), None)
    if current_def:
        st.caption(f"Klimatbudgeten → {current_def['icon']} {current_def['label']}")


def render_hub_footer():
    """Render source attribution and external links for the hub page."""
    st.markdown("---")
    st.caption("Källa: Mål och budget 2026 med plan för 2027–2028, Uppsala kommun")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button(
            "🏛️ Uppsala kommuns klimatbudget",
            "https://www.uppsala.se/kommun-och-politik/kommunens-mal-och-budget/"
            "mal-och-budget/klimatbudget/",
        )
    with col2:
        st.link_button(
            "🔬 Deep Research-rapport",
            "https://gemini.google.com/share/e6409eaadff7",
        )
