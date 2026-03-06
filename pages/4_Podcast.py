"""Podcast — Lyssna på AI-genererade podcastavsnitt om klimatbudgeten."""

import json
import re
from datetime import UTC, datetime
from pathlib import Path

import streamlit as st

from lib.auth import check_password
from lib.favorites import render_sidebar_favorites
from lib.feedback import thumbs_feedback
from lib.nav import render_nav_bar
from lib.style import PALETTE, inject_custom_css

st.set_page_config(
    page_title="Podcast — Klimatbudget",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if not check_password():
    st.stop()

inject_custom_css()
render_sidebar_favorites()
render_nav_bar("podcast")

st.title("🎙️ Podcast: Klimatbudgeten")
st.markdown(
    "AI-genererade podcastavsnitt om Uppsala kommuns klimatbudget. "
    "Perfekt att lyssna på inför möten eller som introduktion för nya medarbetare."
)

# --- Podcast catalog ---
catalog_file = Path("assets/generated/podcast_catalog.json")

if catalog_file.exists():
    with open(catalog_file, encoding="utf-8") as f:
        catalog = json.load(f)
else:
    catalog = []

# Auto-discover MP3 files only (skip WAV duplicates)
audio_dir = Path("assets/generated")
existing_files = {p["file"] for p in catalog}
for audio_file in sorted(audio_dir.glob("podcast*.mp3")):
    if audio_file.name not in existing_files:
        stat = audio_file.stat()
        catalog.append(
            {
                "name": "Klimatbudgeten — djupdykning",
                "description": "En AI-genererad genomgång av Uppsala kommuns klimatbudget.",
                "file": audio_file.name,
                "created": datetime.fromtimestamp(stat.st_mtime, tz=UTC).strftime(
                    "%Y-%m-%d"
                ),
            }
        )

# Check if transcript exists
transcript_file = Path("assets/generated/podcast_transcript.txt")
has_transcript = transcript_file.exists()

# Format signal
if has_transcript:
    st.markdown(
        '<div class="format-bar">'
        "<span>Tillgänglig som:</span> "
        "<span>🎧 Ljud</span> · "
        "<span>📖 Transkript</span>"
        "</div>",
        unsafe_allow_html=True,
    )

# --- Tabs: Listen / Transcript ---
if has_transcript:
    tab_listen, tab_transcript = st.tabs(["🎧 Lyssna", "📖 Transkript"])
else:
    tab_listen = st.container()

# Listen tab
with tab_listen:
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

# Transcript tab
if has_transcript:
    with tab_transcript:
        st.markdown("---")
        st.subheader("📖 Transkript")

        # Inject transcript-specific CSS to override global span color rules
        st.markdown(
            f"""
            <style>
            .tr-ts {{ color: {PALETTE["cream"]} !important; opacity: 0.5; font-size: 0.8rem; }}
            .tr-han {{ color: #9a9a9a !important; }}
            .tr-han-name {{ color: #9a9a9a !important; font-weight: 700; }}
            .tr-hon {{ color: {PALETTE["white"]} !important; }}
            .tr-hon-name {{ color: {PALETTE["white"]} !important; font-weight: 700; }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        transcript_text = transcript_file.read_text(encoding="utf-8")
        lines = transcript_text.strip().splitlines()

        # Parse and render with speaker colors.
        # Only show speaker name when the speaker changes.
        speaker_css = {"Han": "han", "Hon": "hon"}
        prev_speaker = None

        for line in lines:
            match = re.match(r"\[(\d{2}:\d{2})\]\s*(.+?):\s*(.+)", line)
            if match:
                timestamp, speaker, text = match.groups()
                css = speaker_css.get(speaker, "hon")
                # Show speaker name only on first appearance or change
                if speaker != prev_speaker:
                    speaker_html = (
                        f'<span class="tr-{css}-name">{speaker}:</span> '
                    )
                    prev_speaker = speaker
                else:
                    speaker_html = ""
                st.markdown(
                    f'<span class="tr-ts">[{timestamp}]</span> '
                    f"{speaker_html}"
                    f'<span class="tr-{css}">{text}</span>',
                    unsafe_allow_html=True,
                )
            elif line.strip():
                st.markdown(line)

        thumbs_feedback("podcast_transcript", "transkript", key_suffix="pod_tr")

# --- Request new podcast ---
st.markdown("---")
st.subheader("💡 Föreslå nytt podcastavsnitt")
st.markdown(
    "Beskriv vad du vill att nästa podcastavsnitt ska fokusera på. "
    "Förslagen samlas in och genereras sedan via NotebookLM."
)

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
    if requests_file.exists():
        with open(requests_file, encoding="utf-8") as f:
            requests = json.load(f)
    else:
        requests = []

    requests.append(
        {
            "prompt": prompt.strip(),
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
        }
    )

    with open(requests_file, "w", encoding="utf-8") as f:
        json.dump(requests, f, ensure_ascii=False, indent=2)

    st.success(
        "Tack! Ditt förslag har sparats och kommer att genereras vid nästa batch-körning."
    )
    st.caption("💾 Förslaget sparas lokalt i `feedback/podcast_requests.json`.")

# Show pending requests
if requests_file.exists():
    with open(requests_file, encoding="utf-8") as f:
        requests = json.load(f)
    pending = [r for r in requests if r.get("status") == "pending"]
    if pending:
        with st.expander(f"📋 Väntande förslag ({len(pending)} st)"):
            for r in pending:
                ts = r["timestamp"][:10]
                st.markdown(f"- **{ts}**: {r['prompt']}")
