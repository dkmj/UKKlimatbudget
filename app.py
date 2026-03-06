"""Uppsala Klimatbudget — Huvudsida."""

import streamlit as st

from lib.auth import check_password
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

# Layer 1: Hub Hero with SVG Illustration
st.html(
    """
<div class="hub-hero">
    <!-- Minimal SVG illustration: "ett mjöl, sju bröd" -->
    <svg width="200" height="120" viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="100%" x2="0%" y2="0%">
                <stop offset="0%" style="stop-color:#D4A843;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#D94F7A;stop-opacity:1" />
            </linearGradient>
        </defs>
        <!-- Source Base -->
        <circle cx="100" cy="100" r="12" fill="#D4A843" />
        <!-- Branching paths -->
        <path d="M 100 88 C 100 60, 20 50, 20 20" stroke="url(#grad1)" stroke-width="3" fill="none" opacity="0.8"/>
        <path d="M 100 88 C 100 60, 45 45, 45 15" stroke="url(#grad1)" stroke-width="3" fill="none" opacity="0.8"/>
        <path d="M 100 88 C 100 60, 75 40, 75 10" stroke="url(#grad1)" stroke-width="3" fill="none" opacity="0.8"/>
        <path d="M 100 88 C 100 50, 100 30, 100 10" stroke="url(#grad1)" stroke-width="4" fill="none" />
        <path d="M 100 88 C 100 60, 125 40, 125 10" stroke="url(#grad1)" stroke-width="3" fill="none" opacity="0.8"/>
        <path d="M 100 88 C 100 60, 155 45, 155 15" stroke="url(#grad1)" stroke-width="3" fill="none" opacity="0.8"/>
        <path d="M 100 88 C 100 60, 180 50, 180 20" stroke="url(#grad1)" stroke-width="3" fill="none" opacity="0.8"/>
        
        <!-- Nodes for the 7 views -->
        <circle cx="20" cy="20" r="5" fill="#D94F7A" />
        <circle cx="45" cy="15" r="5" fill="#D94F7A" />
        <circle cx="75" cy="10" r="5" fill="#D94F7A" />
        <circle cx="100" cy="10" r="6" fill="#F0EDE8" />
        <circle cx="125" cy="10" r="5" fill="#D94F7A" />
        <circle cx="155" cy="15" r="5" fill="#D94F7A" />
        <circle cx="180" cy="20" r="5" fill="#D94F7A" />
    </svg>
    <h1>Uppsala Klimatbudget</h1>
    <p>Ett dokument. Sju perspektiv.<br>72 klimatåtgärder utforskade på sju olika sätt.</p>
</div>
    """
)

# Layer 2: The Glass Cards Grid
# Row 1 (4 items)
cols1 = st.columns(4)

with cols1[0]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.page_link("pages/1_Översikt.py", label="Översikt", icon="📊")
    st.markdown('<p>Dashboard med nyckeltal</p></div>', unsafe_allow_html=True)

with cols1[1]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.page_link("pages/2_Utforska.py", label="Utforska", icon="🔍")
    st.markdown('<p>Sök och filtrera 72 åtgärder</p></div>', unsafe_allow_html=True)

with cols1[2]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.page_link("pages/3_Quiz.py", label="Quiz", icon="❓")
    st.markdown('<p>Testa din kunskap</p></div>', unsafe_allow_html=True)

with cols1[3]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.page_link("pages/4_Podcast.py", label="Podcast", icon="🎙️")
    st.markdown('<p>Lyssna 🎧 eller Läs 📖</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Row 2 (3 items, centered visually)
# We use 5 columns with empty edges to center the 3 items
cols2 = st.columns([1, 2, 2, 2, 1])

with cols2[1]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.page_link("pages/5_Presentation.py", label="Presentation", icon="📑")
    st.markdown('<p>Bildspel för möten</p></div>', unsafe_allow_html=True)

with cols2[2]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.page_link("pages/6_Chatt.py", label="Chatt", icon="💬")
    st.markdown('<p>Ställ frågor till AI</p></div>', unsafe_allow_html=True)

with cols2[3]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.page_link("pages/7_Rapport.py", label="Rapport", icon="📄")
    st.markdown('<p>PDF 📄 eller Webb 🌐</p></div>', unsafe_allow_html=True)

# Layer 3: Footer Linkroll
st.html(
    """
<div style="text-align: center; max-width: 600px; margin: 40px auto 20px; color: #E8E0D8; font-style: italic; opacity: 0.9;">
    "En källa, många sätt att bearbeta, förstå, tänka kring. Fokus Uppsala kommun klimatbudget 2026"
</div>
<div class="footer-linkroll">
    <span style="color: rgba(232, 224, 216, 0.5); font-weight: bold; margin-right: 10px;">LÄNKAR:</span>
    <a href="https://www.uppsala.se/kommun-och-politik/kommunens-mal-och-budget/mal-och-budget/klimatbudget/" target="_blank">📄 Uppsala.se (Källa) ↗</a>
    <a href="https://uppsala-klimat.streamlit.app" target="_blank">🌍 Webbutgåva ↗</a>
</div>
    """
)
