"""Flashcards — Repetera klimatbudgeten med 57 flashkort."""

import json
import random
import re
from pathlib import Path

import streamlit as st

from lib.auth import check_password
from lib.favorites import render_sidebar_favorites
from lib.feedback import thumbs_feedback
from lib.nav import render_nav_bar
from lib.style import inject_custom_css

st.set_page_config(
    page_title="Flashcards — Klimatbudget",
    page_icon="🃏",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if not check_password():
    st.stop()

inject_custom_css()
render_sidebar_favorites()
render_nav_bar("flashcards")

st.title("🃏 Flashcards: Klimatbudgeten")
st.markdown("Repetera nyckelbegrepp och fakta med flashkort.")


def _strip_latex(text: str) -> str:
    """Remove LaTeX notation: $18-22\\%$ -> 18-22%."""
    text = re.sub(r"\$([^$]+)\$", r"\1", text)
    return text.replace("\\%", "%").replace("\\", "")


# Load flashcard data
flashcards_file = Path("assets/generated/flashcards.json")

if not flashcards_file.exists():
    st.info("Inga flashkort har genererats ännu.")
    st.stop()

with open(flashcards_file, encoding="utf-8") as f:
    fc_data = json.load(f)

cards = fc_data.get("cards", [])
if not cards:
    st.info("Inga flashkort hittades i filen.")
    st.stop()

# Initialize session state
if "fc_page_index" not in st.session_state:
    st.session_state.fc_page_index = 0
    st.session_state.fc_page_revealed = False
    st.session_state.fc_page_order = list(range(len(cards)))
    st.session_state.fc_correct = 0
    st.session_state.fc_incorrect = 0
    st.session_state.fc_rated = False

total = len(cards)
idx = st.session_state.fc_page_index
card_data_idx = st.session_state.fc_page_order[idx]
card = cards[card_data_idx]

# Progress bar
st.progress((idx + 1) / total, text=f"Kort {idx + 1} av {total}")

# Card display — question side
st.markdown(
    f"""
    <div style="background:rgba(45,27,78,0.6);border:1px solid #5B2D8E;
                border-radius:12px;padding:1.5rem;text-align:center;
                min-height:120px;display:flex;align-items:center;
                justify-content:center;margin:1rem 0;">
        <p style="font-size:1.15rem;font-weight:500;color:#F0EDE8;margin:0;">
            {_strip_latex(card["front"])}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Reveal button / answer
if not st.session_state.fc_page_revealed:
    if st.button("🔄 Vänd kort", use_container_width=True, key="fc_reveal"):
        st.session_state.fc_page_revealed = True
        st.session_state.fc_rated = False
        st.rerun()
else:
    st.success(_strip_latex(card["back"]))

    # Self-assessment — did you know the answer?
    if not st.session_state.fc_rated:
        st.markdown("**Kunde du svaret?**")
        col_right, col_wrong = st.columns(2)
        with col_right:
            if st.button("✅ Rätt", use_container_width=True, key="fc_right"):
                st.session_state.fc_correct += 1
                st.session_state.fc_rated = True
                st.rerun()
        with col_wrong:
            if st.button("❌ Fel", use_container_width=True, key="fc_wrong"):
                st.session_state.fc_incorrect += 1
                st.session_state.fc_rated = True
                st.rerun()

# Score display
answered = st.session_state.fc_correct + st.session_state.fc_incorrect
if answered > 0:
    st.caption(
        f"Poäng: ✅ {st.session_state.fc_correct} rätt · "
        f"❌ {st.session_state.fc_incorrect} fel "
        f"({st.session_state.fc_correct}/{answered})"
    )

# Navigation row
def _advance(delta: int):
    st.session_state.fc_page_index += delta
    st.session_state.fc_page_revealed = False
    st.session_state.fc_rated = False

col_prev, col_shuffle, col_next = st.columns([1, 1, 1])

with col_prev:
    if st.button("⬅️ Föregående", disabled=idx == 0, key="fc_prev", use_container_width=True):
        _advance(-1)
        st.rerun()

with col_shuffle:
    if st.button("🔀 Blanda", key="fc_shuffle", use_container_width=True):
        random.shuffle(st.session_state.fc_page_order)
        st.session_state.fc_page_index = 0
        st.session_state.fc_page_revealed = False
        st.session_state.fc_rated = False
        st.rerun()

with col_next:
    if st.button(
        "Nästa ➡️",
        disabled=idx >= total - 1,
        key="fc_next",
        use_container_width=True,
    ):
        _advance(1)
        st.rerun()

# Reset button at the end
if idx == total - 1:
    st.markdown("---")
    if answered > 0:
        pct = round(100 * st.session_state.fc_correct / answered)
        st.success(
            f"Du har gått igenom alla kort! 🎉\n\n"
            f"Resultat: **{st.session_state.fc_correct}/{answered}** rätt ({pct}%)"
        )
    else:
        st.success("Du har gått igenom alla kort! 🎉")
    if st.button("🔁 Starta om", use_container_width=True):
        st.session_state.fc_page_index = 0
        st.session_state.fc_page_revealed = False
        st.session_state.fc_page_order = list(range(len(cards)))
        st.session_state.fc_correct = 0
        st.session_state.fc_incorrect = 0
        st.session_state.fc_rated = False
        st.rerun()

thumbs_feedback("flashcards_page", f"kort_{card_data_idx}", key_suffix=f"fcp_{idx}")
