# -*- coding: utf-8 -*-
"""Presentation — Bildspel för möten och workshops."""

import streamlit as st
from pathlib import Path
from lib.auth import check_password
from lib.feedback import thumbs_feedback

st.set_page_config(page_title="Presentation — Klimatbudget", page_icon="📑", layout="wide")

if not check_password():
    st.stop()

st.title("📑 Presentation: Klimatbudgeten")
st.markdown("AI-genererad presentation som kan användas i möten och workshops.")

# Look for generated slides
slides_dir = Path("assets/generated")
slide_files = list(slides_dir.glob("*.pdf")) + list(slides_dir.glob("*.pptx"))

if slide_files:
    for slide_file in sorted(slide_files):
        st.subheader(slide_file.stem.replace("_", " ").title())

        if slide_file.suffix == ".pdf":
            with open(slide_file, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="📥 Ladda ner presentation (PDF)",
                data=pdf_bytes,
                file_name=slide_file.name,
                mime="application/pdf",
            )
            # Display PDF inline if possible
            import base64

            b64 = base64.b64encode(pdf_bytes).decode()
            st.markdown(
                f'<iframe src="data:application/pdf;base64,{b64}" '
                f'width="100%" height="600" type="application/pdf"></iframe>',
                unsafe_allow_html=True,
            )
        else:
            with open(slide_file, "rb") as f:
                st.download_button(
                    label="📥 Ladda ner presentation (PPTX)",
                    data=f.read(),
                    file_name=slide_file.name,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )

        thumbs_feedback("presentation", slide_file.stem, key_suffix=slide_file.stem)
else:
    st.info("Ingen presentation har genererats ännu.")

# --- Mind Map ---
st.markdown("---")
st.subheader("🧠 Tankekarta")

mind_map_files = list(slides_dir.glob("mind_map*"))
if mind_map_files:
    for mm_file in sorted(mind_map_files):
        if mm_file.suffix == ".html":
            with open(mm_file, "r", encoding="utf-8") as f:
                html_content = f.read()
            import streamlit.components.v1 as components

            components.html(html_content, height=700, scrolling=True)

            with open(mm_file, "rb") as f:
                st.download_button(
                    label="📥 Ladda ner tankekarta (HTML)",
                    data=f.read(),
                    file_name=mm_file.name,
                    mime="text/html",
                )
        thumbs_feedback("mind_map", mm_file.stem, key_suffix=mm_file.stem)
else:
    st.info("Ingen tankekarta har genererats ännu.")
