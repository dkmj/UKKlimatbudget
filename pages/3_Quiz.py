"""Quiz — Testa din kunskap om klimatbudgeten."""

import json
import random
import re
from pathlib import Path

import streamlit as st

from lib.auth import check_password
from lib.favorites import render_sidebar_favorites
from lib.feedback import thumbs_feedback
from lib.style import inject_custom_css

st.set_page_config(page_title="Quiz — Klimatbudget", page_icon="❓", layout="centered")

if not check_password():
    st.stop()

inject_custom_css()
render_sidebar_favorites()

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

# Initialize quiz state
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_answered = False
    st.session_state.quiz_order = list(range(len(quiz_data)))
    random.shuffle(st.session_state.quiz_order)
    # Pre-shuffle options for each question so correct answer isn't always first
    st.session_state.quiz_shuffled_options = {}
    for i in range(len(quiz_data)):
        options = quiz_data[i]["alternativ"].copy()
        random.shuffle(options)
        st.session_state.quiz_shuffled_options[i] = options

total = len(quiz_data)
idx = st.session_state.quiz_index

if idx >= total:
    st.success(f"Quiz klar! Du fick **{st.session_state.quiz_score}/{total}** rätt.")
    thumbs_feedback(
        "quiz", f"Resultat: {st.session_state.quiz_score}/{total}", key_suffix="result"
    )
    if st.button("Starta om"):
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_order = list(range(len(quiz_data)))
        random.shuffle(st.session_state.quiz_order)
        # Re-shuffle options
        st.session_state.quiz_shuffled_options = {}
        for i in range(len(quiz_data)):
            options = quiz_data[i]["alternativ"].copy()
            random.shuffle(options)
            st.session_state.quiz_shuffled_options[i] = options
        st.rerun()
    st.stop()

q_data_idx = st.session_state.quiz_order[idx]
q = quiz_data[q_data_idx]
shuffled_options = st.session_state.quiz_shuffled_options.get(
    q_data_idx, q["alternativ"]
)

st.progress((idx) / total, text=f"Fråga {idx + 1} av {total}")

st.markdown(f"### {q['fråga']}")

selected = st.radio(
    "Välj ditt svar:",
    shuffled_options,
    index=None,
    key=f"quiz_q_{idx}",
    disabled=st.session_state.quiz_answered,
)

if not st.session_state.quiz_answered:
    if selected is None:
        st.caption("👆 Välj ett alternativ ovan för att kunna svara.")
    if st.button("Svara", key=f"quiz_submit_{idx}", disabled=(selected is None)):
        st.session_state.quiz_answered = True
        if selected == q["rätt_svar"]:
            st.session_state.quiz_score += 1
            st.success("Rätt! ✅")
        else:
            st.error(f"Fel. Rätt svar: **{q['rätt_svar']}**")
        st.info(f"💡 {q['förklaring']}")
        st.rerun()
else:
    if selected == q["rätt_svar"]:
        st.success("Rätt! ✅")
    else:
        st.error(f"Fel. Rätt svar: **{q['rätt_svar']}**")
    st.info(f"💡 {q['förklaring']}")

    if st.button("Nästa fråga →", key=f"quiz_next_{idx}"):
        st.session_state.quiz_index += 1
        st.session_state.quiz_answered = False
        st.rerun()
