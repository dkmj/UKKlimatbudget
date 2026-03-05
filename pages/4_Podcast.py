# -*- coding: utf-8 -*-
"""Podcast — Lyssna på AI-genererade podcastavsnitt om klimatbudgeten."""

import json
import streamlit as st
from datetime import datetime
from pathlib import Path
from lib.auth import check_password
from lib.feedback import thumbs_feedback
from lib.favorites import render_sidebar_favorites
from lib.style import inject_custom_css

st.set_page_config(page_title="Podcast — Klimatbudget", page_icon="🎙️", layout="centered")

if not check_password():
    st.stop()

inject_custom_css()
render_sidebar_favorites()

st.title("🎙️ Podcast: Klimatbudgeten")
st.markdown(
    "AI-genererade podcastavsnitt om Uppsala kommuns klimatbudget. "
    "Perfekt att lyssna på inför möten eller som introduktion för nya medarbetare."
)

# --- Podcast catalog ---
# Each podcast entry: {name, description, file, created}
catalog_file = Path("assets/generated/podcast_catalog.json")

# Initialize catalog from existing files if no catalog exists
if catalog_file.exists():
    with open(catalog_file, "r", encoding="utf-8") as f:
        catalog = json.load(f)
else:
    catalog = []

# Auto-discover audio files not in catalog
audio_dir = Path("assets/generated")
existing_files = {p["file"] for p in catalog}
for audio_file in sorted(list(audio_dir.glob("podcast*.wav")) + list(audio_dir.glob("podcast*.mp3"))):
    if audio_file.name not in existing_files:
        stat = audio_file.stat()
        catalog.append({
            "name": "Klimatbudgeten — djupdykning",
            "description": "En AI-genererad genomgång av Uppsala kommuns klimatbudget.",
            "file": audio_file.name,
            "created": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"),
        })

# Display podcasts
if catalog:
    for i, pod in enumerate(catalog):
        audio_path = audio_dir / pod["file"]
        if not audio_path.exists():
            continue

        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"🎧 {pod['name']}")
            if pod.get("description"):
                st.markdown(pod["description"])
        with col2:
            st.caption(f"📅 {pod['created']}")
            size_mb = audio_path.stat().st_size / (1024 * 1024)
            st.caption(f"📦 {size_mb:.1f} MB")

        st.audio(str(audio_path))
        thumbs_feedback("podcast", pod["name"], key_suffix=f"pod_{i}")
else:
    st.info("Inga podcastavsnitt har genererats ännu.")

# --- Request new podcast ---
st.markdown("---")
st.subheader("💡 Föreslå nytt podcastavsnitt")
st.markdown(
    "Beskriv vad du vill att nästa podcastavsnitt ska fokusera på. "
    "Förslagen samlas in och genereras sedan via NotebookLM."
)

# Load existing requests
requests_file = Path("feedback/podcast_requests.json")
requests_file.parent.mkdir(exist_ok=True)

with st.form("podcast_request", clear_on_submit=True):
    prompt = st.text_area(
        "Beskriv fokus för podcastavsnittet:",
        placeholder="T.ex. 'Fokusera på transportåtgärderna och hur spårvägen hänger ihop med cyklingsatsningarna'",
        height=100,
    )
    submitted = st.form_submit_button("📨 Skicka förslag")

if submitted and prompt.strip():
    # Save the request
    if requests_file.exists():
        with open(requests_file, "r", encoding="utf-8") as f:
            requests = json.load(f)
    else:
        requests = []

    requests.append({
        "prompt": prompt.strip(),
        "timestamp": datetime.now().isoformat(),
        "status": "pending",
    })

    with open(requests_file, "w", encoding="utf-8") as f:
        json.dump(requests, f, ensure_ascii=False, indent=2)

    st.success("Tack! Ditt förslag har sparats och kommer att genereras vid nästa batch-körning.")
    st.caption("💾 Förslaget sparas lokalt i `feedback/podcast_requests.json`.")

# Show pending requests
if requests_file.exists():
    with open(requests_file, "r", encoding="utf-8") as f:
        requests = json.load(f)
    pending = [r for r in requests if r.get("status") == "pending"]
    if pending:
        with st.expander(f"📋 Väntande förslag ({len(pending)} st)"):
            for r in pending:
                ts = r["timestamp"][:10]
                st.markdown(f"- **{ts}**: {r['prompt']}")
