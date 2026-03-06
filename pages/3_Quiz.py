"""Quiz — Testa din kunskap om klimatbudgeten."""

import json
import random
import re
from pathlib import Path

import streamlit as st

from lib.auth import check_password
from lib.feedback import thumbs_feedback
from lib.nav import render_top_nav
from lib.style import inject_custom_css

st.set_page_config(page_title="Quiz — Klimatbudget", page_icon="❓", layout="centered", initial_sidebar_state="collapsed")

if not check_password():
    st.stop()

inject_custom_css()
render_top_nav("quiz")

st.title("❓ Quiz: Klimatbudgeten")


def _strip_latex(text: str) -> str:
    """Remove LaTeX notation from text: $18-22\\%$ → 18-22%."""
    text = re.sub(r"\$([^$]+)\$", r"\1", text)
    text = text.replace("\\%", "%").replace("\\", "")
    return text


# Check for NotebookLM-generated quiz
quiz_file = Path("assets/generated/quiz.json")

if quiz_file.exists():
    with open(quiz_file, encoding="utf-8") as f:
        raw = json.load(f)
    # Normalize NLM format → internal format
    if "questions" in raw:
        quiz_data = []
        for q in raw["questions"]:
            # NLM sometimes uses "text" instead of "question"
            question_text = q.get("question", q.get("text", ""))
            correct = next(
                (_strip_latex(a["text"]) for a in q["answerOptions"] if a["isCorrect"]),
                "",
            )
            correct_rationale = next(
                (
                    _strip_latex(a.get("rationale", ""))
                    for a in q["answerOptions"]
                    if a["isCorrect"]
                ),
                "",
            )
            quiz_data.append(
                {
                    "fråga": _strip_latex(question_text),
                    "alternativ": [_strip_latex(a["text"]) for a in q["answerOptions"]],
                    "rätt_svar": correct,
                    "förklaring": correct_rationale,
                }
            )
    else:
        quiz_data = raw
    st.markdown("Testa din kunskap om Uppsala kommuns klimatbudget!")
else:
    # Built-in fallback quiz based on the document
    quiz_data = [
        {
            "fråga": "Vilket år ska Uppsala vara klimatneutralt?",
            "alternativ": ["2025", "2030", "2040", "2050"],
            "rätt_svar": "2030",
            "förklaring": "Uppsala ska vara klimatneutralt år 2030 och klimatpositivt senast 2050.",
        },
        {
            "fråga": "Hur mycket ska växthusgasutsläppen minska per år under planperioden?",
            "alternativ": [
                "5–10 procent",
                "10–15 procent",
                "18–22 procent",
                "25–30 procent",
            ],
            "rätt_svar": "18–22 procent",
            "förklaring": "Utsläppen ska minska med 18–22 procent per år för att utsläppsutrymmet inte ska överskridas.",
        },
        {
            "fråga": "Hur många klimatåtgärder finns totalt i klimatbudgeten?",
            "alternativ": ["32", "52", "72", "92"],
            "rätt_svar": "72",
            "förklaring": "Klimatbudgeten innehåller 72 numrerade åtgärder fördelade på 6 områden.",
        },
        {
            "fråga": "Inom vilket område finns flest klimatåtgärder?",
            "alternativ": ["Energi", "Transport", "Konsumtion", "Bygg och anläggning"],
            "rätt_svar": "Transport",
            "förklaring": "Transport har 23 åtgärder, följt av Energi med 20 åtgärder.",
        },
        {
            "fråga": "Hur stora var de kommungeografiska utsläppen 2023?",
            "alternativ": [
                "516 kton CO₂e",
                "716 kton CO₂e",
                "816 kton CO₂e",
                "916 kton CO₂e",
            ],
            "rätt_svar": "816 kton CO₂e",
            "förklaring": "Utfall 2023: 816 kiloton koldioxidekvivalenter (2022: 807).",
        },
    ]
    st.markdown(
        "Testa din kunskap om Uppsala kommuns klimatbudget! "
        "*(Fler frågor kommer att genereras via NotebookLM.)*"
    )

# --- Flashcard CSS ---
st.markdown("""
<style>
.flashcard-container {
    perspective: 1000px;
    width: 100%;
    max-width: 600px;
    height: 300px;
    margin: 2rem auto;
}
.flashcard {
    width: 100%;
    height: 100%;
    position: relative;
    transition: transform 0.6s;
    transform-style: preserve-3d;
    cursor: pointer;
}
.flashcard.flipped {
    transform: rotateY(180deg);
}
.flashcard-front, .flashcard-back {
    width: 100%;
    height: 100%;
    position: absolute;
    backface-visibility: hidden;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    border: 1px solid rgba(123, 45, 142, 0.4);
}
.flashcard-front {
    background: rgba(45, 27, 78, 0.7);
}
.flashcard-back {
    background: rgba(91, 45, 142, 0.8);
    transform: rotateY(180deg);
}
.flashcard-front h3 {
    margin: 0;
    color: #F0EDE8;
}
.flashcard-back h2 {
    color: #D4A843;
    margin-top: 0;
    margin-bottom: 1rem;
}
.flashcard-back p {
    color: #F0EDE8;
    font-size: 1.1rem;
    margin: 0;
}
.flashcard-hint {
    font-size: 0.8rem;
    opacity: 0.6;
    margin-top: 2rem;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# Initialize flashcard state
if "fc_index" not in st.session_state:
    st.session_state.fc_index = 0
    st.session_state.fc_flipped = False
    st.session_state.fc_order = list(range(len(quiz_data)))
    random.shuffle(st.session_state.fc_order)

total = len(quiz_data)
idx = st.session_state.fc_index

# Navigation and Progress
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Föregående", disabled=(idx == 0), use_container_width=True):
        st.session_state.fc_index -= 1
        st.session_state.fc_flipped = False
        st.rerun()

with col2:
    st.progress((idx + 1) / total, text=f"Flashcard {idx + 1} av {total}")

with col3:
    if st.button("Nästa ➡️", disabled=(idx == total - 1), use_container_width=True):
        st.session_state.fc_index += 1
        st.session_state.fc_flipped = False
        st.rerun()

# Get current question
q_data_idx = st.session_state.fc_order[idx]
q = quiz_data[q_data_idx]

# Toggle flip state button (invisible, triggered by JS if possible, but we use a Streamlit button for actual state)
col_flip1, col_flip2, col_flip3 = st.columns([1, 2, 1])
with col_flip2:
    flip_label = "Vänd tillbaka kortet 🔄" if st.session_state.fc_flipped else "Visa svaret 🔄"
    if st.button(flip_label, use_container_width=True):
        st.session_state.fc_flipped = not st.session_state.fc_flipped
        st.rerun()

# Render the Flashcard
flipped_class = "flipped" if st.session_state.fc_flipped else ""

st.markdown(f"""
<div class="flashcard-container">
    <div class="flashcard {flipped_class}">
        <div class="flashcard-front">
            <h3>{q['fråga']}</h3>
            <div class="flashcard-hint">Klicka på knappen ovan för att se svaret</div>
        </div>
        <div class="flashcard-back">
            <h2>{q['rätt_svar']}</h2>
            <p>{q['förklaring']}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("Slumpa om korten 🔀"):
    st.session_state.fc_index = 0
    st.session_state.fc_flipped = False
    random.shuffle(st.session_state.fc_order)
    st.rerun()
