"""Chatt — Ställ frågor och brainstorma kring klimatbudgeten."""

import json

import streamlit as st

from lib.auth import check_password
from lib.favorites import render_sidebar_favorites
from lib.feedback import thumbs_feedback
from lib.nav import render_nav_bar
from lib.rate_limit import check_rate_limit, increment_request
from lib.style import inject_custom_css

st.set_page_config(
    page_title="Chatt — Klimatbudget",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if not check_password():
    st.stop()

inject_custom_css()
render_sidebar_favorites()
render_nav_bar("chatt")

st.title("💬 Chatt: Klimatbudgeten")

# Load document context
with open("data/klimatbudget.json", encoding="utf-8") as f:
    kb_data = json.load(f)

with open("data/abbreviations.json", encoding="utf-8") as f:
    abbrevs = json.load(f)


def _build_context() -> str:
    """Build document context string for the LLM."""
    lines = ["Uppsala kommuns klimatbudget — sammanfattning:\n"]
    meta = kb_data["meta"]
    lines.append(
        f"Mål: Klimatneutralt {meta['mål_klimatneutral']}, klimatpositivt {meta['mål_klimatpositiv']}."
    )
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


# --- Rate limit check ---
allowed, used_today, daily_limit = check_rate_limit()

if not allowed:
    st.error(
        f"🛑 Daglig gräns nådd ({daily_limit} frågor). Chatten öppnar igen imorgon."
    )
    st.caption(f"Användning idag: {used_today}/{daily_limit}")
    st.stop()

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
    "eller brainstorma kring prioriteringar.  \n"
    "AI är en förhållandevis enkel och billig modell, "
    "därmed inte så djup eller snabb tyvärr."
)
st.caption(f"📊 Frågor idag: {used_today}/{daily_limit}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show suggestions when chat is empty
if not st.session_state.messages:
    st.markdown("---")
    st.markdown("**💡 Prova att fråga:**")
    _suggestions = [
        "Vilka åtgärder har störst potential att minska utsläppen snabbt?",
        "Jämför transportområdet med energiområdet — likheter och skillnader?",
        "Vilka åtgärder kan KS driva utan att behöva samverka med andra?",
        "Hur hänger bygg- och anläggningsåtgärderna ihop med energiåtgärderna?",
        "Brainstorma: vilka nya åtgärder saknas i klimatbudgeten?",
    ]
    _cols = st.columns(2)
    for _i, _s in enumerate(_suggestions):
        with _cols[_i % 2]:
            if st.button(f"💬 {_s}", key=f"sug_{_i}", use_container_width=True):
                st.session_state._pending_prompt = _s
                st.rerun()

SYSTEM_PROMPT = (
    "Du är en expert på Uppsala kommuns klimatbudget. "
    "Svara alltid på svenska. "
    "Basera dina svar på dokumentet nedan. "
    "Var tydlig, konkret och hänvisa till specifika åtgärdsnummer (t.ex. 1.05) när det är relevant. "
    "Om du ombeds brainstorma, var kreativ men håll dig förankrad i dokumentets kontext.\n\n"
    f"DOKUMENT:\n{_build_context()}"
)

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            thumbs_feedback("chatt", msg["content"][:50], key_suffix=f"chat_{i}")

# Model info (shown below the chat input area)
st.caption("Gemini 2.5 Flash · Free Tier: 15 req/min, 1 500 req/dag, 1M tokens/dag")

# Chat input — accept typed prompt or pending suggestion click
prompt = st.chat_input("Ställ en fråga om klimatbudgeten...")
if not prompt and "_pending_prompt" in st.session_state:
    prompt = st.session_state.pop("_pending_prompt")

if prompt:
    # Re-check rate limit before making the API call
    allowed, used_today, daily_limit = check_rate_limit()
    if not allowed:
        st.error(f"🛑 Daglig gräns nådd ({daily_limit}). Försök igen imorgon.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Tänker..."):
            try:
                # Gemini expects role "model", not "assistant"
                history = [
                    {
                        "role": "model" if m["role"] == "assistant" else m["role"],
                        "parts": [m["content"]],
                    }
                    for m in st.session_state.messages[:-1]
                ]
                chat = model.start_chat(history=history)
                response = chat.send_message(
                    f"SYSTEM: {SYSTEM_PROMPT}\n\nUSER: {prompt}"
                )
                answer = response.text
                increment_request()
            except Exception as e:
                err = str(e).lower()
                if "quota" in err or "rate" in err or "429" in err:
                    answer = (
                        "⏳ **För många anrop just nu.** "
                        "Vänta en minut och försök igen."
                    )
                elif "api key" in err or "authenticate" in err or "401" in err:
                    answer = (
                        "🔑 **API-nyckelfel.** "
                        "Kontrollera att din Gemini-nyckel är giltig."
                    )
                elif "timeout" in err or "deadline" in err:
                    answer = (
                        "⌛ **Tidsgräns överskreds.** "
                        "Försök igen med en kortare fråga."
                    )
                else:
                    answer = (
                        "⚠️ **Något gick fel.** "
                        "Försök igen om en stund. "
                        f"(Teknisk info: {type(e).__name__})"
                    )

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        thumbs_feedback(
            "chatt",
            answer[:50],
            key_suffix=f"chat_{len(st.session_state.messages)}",
        )
