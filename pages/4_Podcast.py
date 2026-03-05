# -*- coding: utf-8 -*-
"""Podcast — Lyssna på en AI-genererad genomgång."""

import streamlit as st
from pathlib import Path
from lib.auth import check_password
from lib.feedback import thumbs_feedback

st.set_page_config(page_title="Podcast — Klimatbudget", page_icon="🎙️", layout="centered")

if not check_password():
    st.stop()

st.title("🎙️ Podcast: Klimatbudgeten")
st.markdown(
    "En AI-genererad djupdykning i Uppsala kommuns klimatbudget. "
    "Perfekt att lyssna på inför möten eller som introduktion för nya medarbetare."
)

# Look for generated audio files
audio_dir = Path("assets/generated")
audio_files = list(audio_dir.glob("*.wav")) + list(audio_dir.glob("*.mp3"))

if audio_files:
    for audio_file in sorted(audio_files):
        st.subheader(audio_file.stem.replace("_", " ").title())
        st.audio(str(audio_file))
        thumbs_feedback("podcast", audio_file.stem, key_suffix=audio_file.stem)
else:
    st.warning(
        "Inget podcastavsnitt har genererats ännu.\n\n"
        "Kör följande för att generera:\n"
        "```bash\n"
        "notebooklm use <notebook-id>\n"
        "notebooklm generate audio \"djupdykning i klimatbudgeten på svenska\"\n"
        "notebooklm download audio -o assets/generated/podcast.wav\n"
        "```"
    )
    st.info(
        "Podcasten kommer att vara en AI-genererad sammanfattning av hela "
        "klimatbudgeten, med fokus på de viktigaste åtgärderna och utmaningarna."
    )
