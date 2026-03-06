"""Uppsala Klimatbudget — Hub page (Bageriet)."""

import streamlit as st

from lib.auth import check_password
from lib.nav import render_hub_footer
from lib.style import inject_custom_css

st.set_page_config(
    page_title="Uppsala Klimatbudget",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if not check_password():
    st.stop()

inject_custom_css()

# --- Hero ---
st.markdown(
    """
    <div class="hub-hero">
        <h1>🌍 Klimatbudgeten</h1>
        <p class="hub-tagline">Ett dokument. Åtta perspektiv.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- SVG illustration: one source → many views ---
st.markdown(
    """
    <div style="text-align:center;margin:0 auto 1.5rem;max-width:600px;">
    <svg viewBox="0 0 520 200" xmlns="http://www.w3.org/2000/svg"
         style="width:100%;max-width:550px;">
      <!-- Central source -->
      <circle cx="260" cy="100" r="32" fill="#D4A843" opacity="0.9"/>
      <text x="260" y="96" text-anchor="middle" fill="#1A0A2E"
            font-size="10" font-weight="700">Mål &amp;</text>
      <text x="260" y="108" text-anchor="middle" fill="#1A0A2E"
            font-size="10" font-weight="700">Budget</text>

      <!-- Rays + outer circles -->
      <line x1="260" y1="100" x2="60"  y2="50"  stroke="#7B2D8E" stroke-width="1.5" opacity="0.5"/>
      <line x1="260" y1="100" x2="130" y2="30"  stroke="#D94F7A" stroke-width="1.5" opacity="0.5"/>
      <line x1="260" y1="100" x2="200" y2="20"  stroke="#D4A843" stroke-width="1.5" opacity="0.5"/>
      <line x1="260" y1="100" x2="320" y2="20"  stroke="#8B9B58" stroke-width="1.5" opacity="0.5"/>
      <line x1="260" y1="100" x2="390" y2="30"  stroke="#5B2D8E" stroke-width="1.5" opacity="0.5"/>
      <line x1="260" y1="100" x2="460" y2="50"  stroke="#E8476C" stroke-width="1.5" opacity="0.5"/>
      <line x1="260" y1="100" x2="460" y2="150" stroke="#6B7D3A" stroke-width="1.5" opacity="0.5"/>
      <line x1="260" y1="100" x2="60"  y2="150" stroke="#D4A843" stroke-width="1.5" opacity="0.5"/>

      <!-- Outer nodes -->
      <circle cx="60"  cy="50"  r="18" fill="#7B2D8E" opacity="0.85"/>
      <text x="60"  y="54" text-anchor="middle" fill="#F0EDE8" font-size="14">📊</text>

      <circle cx="130" cy="30"  r="18" fill="#D94F7A" opacity="0.85"/>
      <text x="130" y="34" text-anchor="middle" fill="#F0EDE8" font-size="14">🔍</text>

      <circle cx="200" cy="20"  r="18" fill="#D4A843" opacity="0.85"/>
      <text x="200" y="24" text-anchor="middle" fill="#F0EDE8" font-size="14">❓</text>

      <circle cx="320" cy="20"  r="18" fill="#8B9B58" opacity="0.85"/>
      <text x="320" y="24" text-anchor="middle" fill="#F0EDE8" font-size="14">🎙️</text>

      <circle cx="390" cy="30"  r="18" fill="#5B2D8E" opacity="0.85"/>
      <text x="390" y="34" text-anchor="middle" fill="#F0EDE8" font-size="14">📑</text>

      <circle cx="460" cy="50"  r="18" fill="#E8476C" opacity="0.85"/>
      <text x="460" y="54" text-anchor="middle" fill="#F0EDE8" font-size="14">💬</text>

      <circle cx="460" cy="150" r="18" fill="#6B7D3A" opacity="0.85"/>
      <text x="460" y="154" text-anchor="middle" fill="#F0EDE8" font-size="14">📄</text>

      <circle cx="60"  cy="150" r="18" fill="#D4A843" opacity="0.85"/>
      <text x="60"  y="154" text-anchor="middle" fill="#F0EDE8" font-size="14">🃏</text>
    </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Card definitions ---
CARDS = [
    {
        "icon": "📊",
        "title": "Översikt",
        "desc": "Dashboard med nyckeltal och visualiseringar",
        "path": "pages/1_Översikt.py",
        "accent": "#7B2D8E",
    },
    {
        "icon": "🔍",
        "title": "Utforska",
        "desc": "Sök och filtrera bland alla 72 åtgärder",
        "path": "pages/2_Utforska.py",
        "accent": "#D94F7A",
    },
    {
        "icon": "❓",
        "title": "Quiz",
        "desc": "Testa din kunskap om klimatbudgeten",
        "path": "pages/3_Quiz.py",
        "accent": "#D4A843",
    },
    {
        "icon": "🎙️📖",
        "title": "Podcast",
        "desc": "Lyssna eller läs transkript",
        "path": "pages/4_Podcast.py",
        "accent": "#8B9B58",
    },
    {
        "icon": "📑",
        "title": "Presentation",
        "desc": "Bildspel och begreppsträd",
        "path": "pages/5_Presentation.py",
        "accent": "#5B2D8E",
    },
    {
        "icon": "💬",
        "title": "Chatt",
        "desc": "Fråga AI om klimatbudgeten",
        "path": "pages/6_Chatt.py",
        "accent": "#E8476C",
    },
    {
        "icon": "📄🌐",
        "title": "Rapport",
        "desc": "Djupanalys — PDF och webb",
        "path": "pages/7_Rapport.py",
        "accent": "#6B7D3A",
    },
    {
        "icon": "🃏",
        "title": "Flashcards",
        "desc": "57 flashkort för snabb repetition",
        "path": "pages/8_Flashcards.py",
        "accent": "#D4A843",
    },
]

# --- Card grid: 4 + 4 ---
for row_start in (0, 4):
    cols = st.columns(4)
    for i, col in enumerate(cols):
        card = CARDS[row_start + i]
        with col:
            st.markdown(
                f'<div class="hub-card" style="--accent-color:{card["accent"]}">'
                f'<div class="hub-icon">{card["icon"]}</div>'
                f'<p class="hub-title">{card["title"]}</p>'
                f'<p class="hub-desc">{card["desc"]}</p>'
                f"</div>",
                unsafe_allow_html=True,
            )
            st.page_link(card["path"], label=f"Öppna {card['title']}", use_container_width=True)

# --- Footer ---
render_hub_footer()
