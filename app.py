"""Uppsala Klimatbudget — Huvudsida."""

import streamlit as st

from lib.auth import check_password
from lib.favorites import render_sidebar_favorites
from lib.style import inject_custom_css

st.set_page_config(
    page_title="Uppsala Klimatbudget",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not check_password():
    st.stop()

inject_custom_css()
render_sidebar_favorites()

st.title("Uppsala Klimatbudget")
st.markdown(
    """
    Välkommen till den interaktiva utforskaren av Uppsala kommuns klimatbudget.

    Klimatbudgeten är ett verktyg för att underlätta och påskynda omställningen
    så att klimatmålen kan nås. Den omfattar **72 klimatåtgärder** inom
    **6 områden** som tillsammans ska leda till att Uppsala blir
    **klimatneutralt år 2030** och **klimatpositivt senast 2050**.

    ---

    **Använd menyn till vänster för att:**
    """
)

cols = st.columns(3)
with cols[0]:
    st.markdown(
        """
        **📊 Översikt**
        Dashboard med nyckeltal och visualiseringar

        **🔍 Utforska**
        Sök och filtrera bland alla 72 åtgärder
        """
    )
with cols[1]:
    st.markdown(
        """
        **❓ Quiz**
        Testa din kunskap om klimatbudgeten

        **🎙️ Podcast**
        Lyssna på en AI-genererad genomgång
        """
    )
with cols[2]:
    st.markdown(
        """
        **📑 Presentation**
        Bildspel för möten och workshops

        **💬 Chatt**
        Ställ frågor och brainstorma
        """
    )

st.markdown("---")
st.caption("Källa: Mål och budget 2026 med plan för 2027–2028, Uppsala kommun")
