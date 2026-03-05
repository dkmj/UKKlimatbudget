# -*- coding: utf-8 -*-
"""Chatt — Ställ frågor och brainstorma kring klimatbudgeten."""

import json
import streamlit as st
from lib.auth import check_password
from lib.feedback import thumbs_feedback
from lib.style import inject_custom_css

st.set_page_config(page_title="Chatt — Klimatbudget", page_icon="💬", layout="centered")

if not check_password():
    st.stop()

inject_custom_css()

st.title("💬 Chatt: Klimatbudgeten")

# Load document context
with open("data/klimatbudget.json", "r", encoding="utf-8") as f:
    kb_data = json.load(f)

with open("data/abbreviations.json", "r", encoding="utf-8") as f:
    abbrevs = json.load(f)


def _build_context() -> str:
    """Build document context string for the LLM."""
    lines = ["Uppsala kommuns klimatbudget — sammanfattning:\n"]
    meta = kb_data["meta"]
    lines.append(f"Mål: Klimatneutralt {meta['mål_klimatneutral']}, klimatpositivt {meta['mål_klimatpositiv']}.")
    lines.append(f"Årlig utsläppsminskning: {meta['årlig_minskning_procent']}%.")
    lines.append(f"Utsläpp 2023: {meta['utsläpp_2023_kton']} kton CO₂e.\n")

    for o in kb_data["områden"]:
        lines.append(f"\n## {o['namn']}")
        lines.append(o["beskrivning"])
        for a in o["åtgärder"]:
            ansvariga = ", ".join(a["ansvariga"])
            lines.append(f"  {a['nr']}: {a['åtgärd']} (Ansvariga: {ansvariga})")

    lines.append("\n\nFörkortningar:")
    for k, v in abbrevs.items():
        lines.append(f"  {k} = {v}")

    return "\n".join(lines)


# Try to use Gemini
gemini_available = False
try:
    api_key = st.secrets["gemini_api_key"]
    if api_key:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        gemini_available = True
except Exception:
    api_key = ""

if not gemini_available:
    st.warning("⚠️ Chatten kräver en **Gemini API-nyckel** för att fungera.")

    with st.expander("🔑 Så här skapar du en API-nyckel", expanded=True):
        st.markdown(
            "1. Gå till [Google AI Studio](https://aistudio.google.com/apikey)\n"
            "2. Logga in med ditt Google-konto\n"
            "3. Klicka **Create API key** och välj ett projekt\n"
            "4. Kopiera nyckeln\n\n"
            "**Lokalt:** Skapa filen `.streamlit/secrets.toml` och lägg till:\n"
        )
        st.code('gemini_api_key = "din-nyckel-här"', language="toml")
        st.markdown(
            "**Streamlit Cloud:** Gå till appens inställningar → *Secrets* "
            "och lägg till samma rad."
        )

    st.markdown("---")
    st.markdown("### 💡 Förslag på frågor att ställa (när chatten är aktiv):")
    suggestions = [
        "Vilka åtgärder har störst potential att minska utsläppen snabbt?",
        "Jämför transportområdet med energiområdet — likheter och skillnader?",
        "Vilka åtgärder kan KS driva utan att behöva samverka med andra?",
        "Hur hänger bygg- och anläggningsåtgärderna ihop med energiåtgärderna?",
        "Brainstorma: vilka nya åtgärder saknas i klimatbudgeten?",
    ]
    for s in suggestions:
        st.markdown(f"- {s}")
    st.stop()

# --- Chat interface ---
st.markdown(
    "Ställ frågor om klimatbudgeten, be om analyser, jämförelser "
    "eller brainstorma kring prioriteringar."
)

SYSTEM_PROMPT = (
    "Du är en expert på Uppsala kommuns klimatbudget. "
    "Svara alltid på svenska. "
    "Basera dina svar på dokumentet nedan. "
    "Var tydlig, konkret och hänvisa till specifika åtgärdsnummer (t.ex. 1.05) när det är relevant. "
    "Om du ombeds brainstorma, var kreativ men håll dig förankrad i dokumentets kontext.\n\n"
    f"DOKUMENT:\n{_build_context()}"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            thumbs_feedback("chatt", msg["content"][:50], key_suffix=f"chat_{i}")

# Chat input
if prompt := st.chat_input("Ställ en fråga om klimatbudgeten..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Tänker..."):
            try:
                history = [
                    {"role": m["role"], "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ]
                chat = model.start_chat(history=history)
                response = chat.send_message(
                    f"SYSTEM: {SYSTEM_PROMPT}\n\nUSER: {prompt}"
                )
                answer = response.text
            except Exception as e:
                answer = f"Ett fel uppstod: {e}"

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        thumbs_feedback(
            "chatt",
            answer[:50],
            key_suffix=f"chat_{len(st.session_state.messages)}",
        )
