"""Rapport — Deep Research-rapport om AI-stöd för klimatbudgeten."""

import base64

import streamlit as st
import streamlit.components.v1 as components

from lib.auth import check_password
from lib.favorites import REPORT_PDF_PATH, REPORT_WEB_URL, render_sidebar_favorites
from lib.nav import render_nav_bar
from lib.style import inject_custom_css

st.set_page_config(
    page_title="Rapport — Klimatbudget",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if not check_password():
    st.stop()

inject_custom_css()
render_sidebar_favorites()
render_nav_bar("rapport")

st.title("📄 AI-stöd för Uppsalas klimatbudget")

# Format signal
st.markdown(
    '<div class="format-bar">'
    "<span>Tillgänglig som:</span> "
    "<span>📄 Inline PDF</span> · "
    "<span>⬇️ Nedladdning</span> · "
    "<span>🌐 Webb</span>"
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "Strategisk optimering och AI-drivet beslutsstöd — "
    "en djupanalys genererad med Gemini Deep Research."
)

col1, col2 = st.columns(2)
with col1:
    st.link_button("🌐 Läs på webben (Gemini)", REPORT_WEB_URL)
with col2:
    if REPORT_PDF_PATH.exists():
        st.download_button(
            label="⬇️ Ladda ner PDF",
            data=REPORT_PDF_PATH.read_bytes(),
            file_name="AI-stöd för Uppsalas Klimatbudget.pdf",
            mime="application/pdf",
            key="rapport_download",
        )

st.markdown("---")

# --- Inline PDF viewer using pdf.js ---
if REPORT_PDF_PATH.exists():
    pdf_b64 = base64.b64encode(REPORT_PDF_PATH.read_bytes()).decode()

    viewer_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #1A0A2E;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            padding: 16px 0;
        }}
        canvas {{
            max-width: 100%;
            box-shadow: 0 2px 12px rgba(0,0,0,0.4);
            border-radius: 4px;
        }}
        .page-label {{
            color: #E8E0D8;
            font-family: sans-serif;
            font-size: 13px;
            opacity: 0.6;
            margin-top: 8px;
        }}
    </style>
    </head>
    <body>
    <script>
        pdfjsLib.GlobalWorkerOptions.workerSrc =
            'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

        const pdfData = atob("{pdf_b64}");
        const loadingTask = pdfjsLib.getDocument({{data: pdfData}});

        loadingTask.promise.then(pdf => {{
            for (let i = 1; i <= pdf.numPages; i++) {{
                pdf.getPage(i).then(page => {{
                    const scale = 1.8;
                    const viewport = page.getViewport({{scale}});
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    canvas.width = viewport.width;
                    canvas.height = viewport.height;

                    const label = document.createElement('div');
                    label.className = 'page-label';
                    label.textContent = 'Sida ' + i + ' av ' + pdf.numPages;

                    document.body.appendChild(label);
                    document.body.appendChild(canvas);

                    page.render({{canvasContext: ctx, viewport}});
                }});
            }}
        }});
    </script>
    </body>
    </html>
    """
    components.html(viewer_html, height=12000, scrolling=True)
else:
    st.warning("PDF-filen hittades inte.")
