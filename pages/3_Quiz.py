# -*- coding: utf-8 -*-
"""Quiz — Testa din kunskap om klimatbudgeten."""

import json
import random
import streamlit as st
from lib.auth import check_password
from lib.feedback import thumbs_feedback
from pathlib import Path

st.set_page_config(page_title="Quiz — Klimatbudget", page_icon="❓", layout="centered")

if not check_password():
    st.stop()

st.title("❓ Quiz: Klimatbudgeten")

# Check for NotebookLM-generated quiz
quiz_file = Path("assets/generated/quiz.json")

if quiz_file.exists():
    with open(quiz_file, "r", encoding="utf-8") as f:
        raw = json.load(f)
    # Normalize NLM format → internal format
    if "questions" in raw:
        quiz_data = []
        for q in raw["questions"]:
            correct = next(
                (a["text"] for a in q["answerOptions"] if a["isCorrect"]), ""
            )
            correct_rationale = next(
                (a["rationale"] for a in q["answerOptions"] if a["isCorrect"]), ""
            )
            quiz_data.append({
                "fråga": q["question"],
                "alternativ": [a["text"] for a in q["answerOptions"]],
                "rätt_svar": correct,
                "förklaring": correct_rationale,
            })
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
            "alternativ": ["5–10 procent", "10–15 procent", "18–22 procent", "25–30 procent"],
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
            "alternativ": ["516 kton CO₂e", "716 kton CO₂e", "816 kton CO₂e", "916 kton CO₂e"],
            "rätt_svar": "816 kton CO₂e",
            "förklaring": "Utfall 2023: 816 kiloton koldioxidekvivalenter (2022: 807).",
        },
        {
            "fråga": "Hur mycket köper Uppsala kommun in varor och tjänster för per år?",
            "alternativ": ["1–2 miljarder kr", "3–4 miljarder kr", "5–6 miljarder kr", "8–10 miljarder kr"],
            "rätt_svar": "5–6 miljarder kr",
            "förklaring": "Uppsala kommun köper in varor och tjänster för cirka 5–6 miljarder kronor per år.",
        },
        {
            "fråga": "Vad är målet för andelen resor med gång, cykel eller kollektivtrafik till 2028?",
            "alternativ": ["60 procent", "67 procent", "72 procent", "77 procent"],
            "rätt_svar": "77 procent",
            "förklaring": "Andel resor med gång, cykel eller kollektivtrafik ska öka till 77 procent senast 2028. Utfall 2024 var 59 procent.",
        },
        {
            "fråga": "Vilken organisation ansvarar för flest klimatåtgärder?",
            "alternativ": ["GSN", "KS (Kommunstyrelsen)", "PBN", "UHEM"],
            "rätt_svar": "KS (Kommunstyrelsen)",
            "förklaring": "Kommunstyrelsen (KS) är ansvarig eller medansvarig för det största antalet klimatåtgärder.",
        },
        {
            "fråga": "Vad innebär CCS/CCU som nämns i energiåtgärderna?",
            "alternativ": [
                "Central Climate System",
                "Carbon Capture and Storage/Utilization",
                "Community Climate Standard",
                "Circular Carbon Supply",
            ],
            "rätt_svar": "Carbon Capture and Storage/Utilization",
            "förklaring": "CCS (Carbon Capture and Storage) och CCU (Carbon Capture and Utilization) handlar om infångning och lagring eller användning av koldioxid.",
        },
        {
            "fråga": "Hur många hektar områdesskydd ska kommunen öka med per år?",
            "alternativ": ["10 hektar", "50 hektar", "100 hektar", "200 hektar"],
            "rätt_svar": "100 hektar",
            "förklaring": "Tillskapat områdesskydd (naturreservat och naturvårdsavtal) ska öka genomsnittligen med 100 hektar per år. Utfall 2024: 0 hektar.",
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

total = len(quiz_data)
idx = st.session_state.quiz_index

if idx >= total:
    st.success(
        f"Quiz klar! Du fick **{st.session_state.quiz_score}/{total}** rätt."
    )
    thumbs_feedback("quiz", f"Resultat: {st.session_state.quiz_score}/{total}", key_suffix="result")
    if st.button("Starta om"):
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False
        random.shuffle(st.session_state.quiz_order)
        st.rerun()
    st.stop()

q = quiz_data[st.session_state.quiz_order[idx]]
st.progress((idx) / total, text=f"Fråga {idx + 1} av {total}")

st.markdown(f"### {q['fråga']}")

selected = st.radio(
    "Välj ditt svar:",
    q["alternativ"],
    key=f"quiz_q_{idx}",
    disabled=st.session_state.quiz_answered,
)

if not st.session_state.quiz_answered:
    if st.button("Svara", key=f"quiz_submit_{idx}"):
        st.session_state.quiz_answered = True
        if selected == q["rätt_svar"]:
            st.session_state.quiz_score += 1
            st.success(f"Rätt! ✅")
        else:
            st.error(f"Fel. Rätt svar: **{q['rätt_svar']}**")
        st.info(f"💡 {q['förklaring']}")
        st.rerun()
else:
    if selected == q["rätt_svar"]:
        st.success(f"Rätt! ✅")
    else:
        st.error(f"Fel. Rätt svar: **{q['rätt_svar']}**")
    st.info(f"💡 {q['förklaring']}")

    if st.button("Nästa fråga →", key=f"quiz_next_{idx}"):
        st.session_state.quiz_index += 1
        st.session_state.quiz_answered = False
        st.rerun()
