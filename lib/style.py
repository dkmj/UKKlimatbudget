# -*- coding: utf-8 -*-
"""Shared styling — background image and color palette from Flower Wild photo."""

import base64
import streamlit as st
from pathlib import Path

# Color palette extracted from C.Schubert's "Flower Wild" photograph
PALETTE = {
    "deep_purple": "#1A0A2E",
    "purple": "#2D1B4E",
    "violet": "#5B2D8E",
    "magenta": "#7B2D8E",
    "pink": "#D94F7A",
    "rose": "#E8476C",
    "white": "#F0EDE8",
    "cream": "#E8E0D8",
    "gold": "#D4A843",
    "green": "#8B9B58",
    "olive": "#6B7D3A",
}


def inject_custom_css():
    """Inject global CSS with background image and color palette."""
    bg_path = Path("assets/background.jpg")

    bg_css = ""
    if bg_path.exists():
        b64 = base64.b64encode(bg_path.read_bytes()).decode()
        bg_css = f"""
        [data-testid="stApp"] {{
            background-image: url("data:image/jpeg;base64,{b64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        """

    st.markdown(
        f"""
        <style>
        {bg_css}

        /* Semi-transparent overlay for readability */
        [data-testid="stMain"] {{
            background: rgba(26, 10, 46, 0.88);
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: rgba(45, 27, 78, 0.95) !important;
        }}
        [data-testid="stSidebar"] a {{
            color: {PALETTE["cream"]} !important;
        }}
        [data-testid="stSidebar"] a:hover {{
            color: {PALETTE["pink"]} !important;
        }}

        /* Headings */
        h1, h2, h3 {{
            color: {PALETTE["white"]} !important;
        }}

        /* Body text */
        p, li, span, label, .stMarkdown {{
            color: {PALETTE["cream"]} !important;
        }}

        /* Links */
        a {{
            color: {PALETTE["pink"]} !important;
        }}
        a:hover {{
            color: {PALETTE["rose"]} !important;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {PALETTE["violet"]} !important;
            color: {PALETTE["white"]} !important;
            border: 1px solid {PALETTE["magenta"]} !important;
            border-radius: 8px !important;
        }}
        .stButton > button:hover {{
            background-color: {PALETTE["magenta"]} !important;
            border-color: {PALETTE["pink"]} !important;
        }}

        /* Download buttons */
        .stDownloadButton > button {{
            background-color: {PALETTE["purple"]} !important;
            color: {PALETTE["white"]} !important;
            border: 1px solid {PALETTE["violet"]} !important;
        }}

        /* Metrics */
        [data-testid="stMetricValue"] {{
            color: {PALETTE["white"]} !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {PALETTE["cream"]} !important;
        }}
        [data-testid="stMetricDelta"] {{
            color: {PALETTE["gold"]} !important;
        }}

        /* Cards / containers */
        [data-testid="stExpander"] {{
            background-color: rgba(45, 27, 78, 0.7) !important;
            border: 1px solid {PALETTE["violet"]} !important;
            border-radius: 8px !important;
        }}

        /* Info/Success/Error boxes */
        .stAlert {{
            background-color: rgba(45, 27, 78, 0.8) !important;
            border-radius: 8px !important;
        }}

        /* Radio buttons and checkboxes */
        .stRadio label, .stCheckbox label {{
            color: {PALETTE["cream"]} !important;
        }}

        /* Text input */
        .stTextInput input, .stTextArea textarea {{
            background-color: rgba(45, 27, 78, 0.6) !important;
            color: {PALETTE["white"]} !important;
            border-color: {PALETTE["violet"]} !important;
        }}

        /* Select boxes */
        .stSelectbox > div > div {{
            background-color: rgba(45, 27, 78, 0.6) !important;
            color: {PALETTE["white"]} !important;
        }}

        /* Progress bar */
        .stProgress > div > div {{
            background-color: {PALETTE["magenta"]} !important;
        }}

        /* Chat input */
        [data-testid="stChatInput"] {{
            background-color: rgba(45, 27, 78, 0.8) !important;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab"] {{
            color: {PALETTE["cream"]} !important;
        }}
        .stTabs [aria-selected="true"] {{
            color: {PALETTE["pink"]} !important;
        }}

        /* Data frames */
        .stDataFrame {{
            background-color: rgba(45, 27, 78, 0.6) !important;
        }}

        /* Captions */
        .stCaption, caption {{
            color: {PALETTE["cream"]} !important;
            opacity: 0.8;
        }}

        /* Photo credit */
        .photo-credit {{
            position: fixed;
            bottom: 8px;
            right: 12px;
            font-size: 11px;
            color: rgba(240, 237, 232, 0.4);
            z-index: 999;
        }}

        /* Form styling */
        [data-testid="stForm"] {{
            background-color: rgba(45, 27, 78, 0.5) !important;
            border: 1px solid {PALETTE["violet"]} !important;
            border-radius: 8px !important;
            padding: 1rem !important;
        }}

        /* Multiselect */
        .stMultiSelect > div {{
            background-color: rgba(45, 27, 78, 0.6) !important;
        }}

        /* Audio player - keep default styling */

        /* Chat message bubbles — ensure contrast against background */
        [data-testid="stChatMessage"] {{
            background-color: rgba(45, 27, 78, 0.85) !important;
            border: 1px solid {PALETTE["violet"]} !important;
            border-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            margin-bottom: 0.5rem !important;
        }}
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] span {{
            color: {PALETTE["white"]} !important;
        }}

        /* Hide the default "app" page label in sidebar navigation */
        [data-testid="stSidebarNav"] li:first-child {{
            display: none !important;
        }}

        /* Horizontal rule */
        hr {{
            border-color: {PALETTE["violet"]} !important;
            opacity: 0.5;
        }}
        </style>

        <div class="photo-credit">📷 C.Schubert</div>
        """,
        unsafe_allow_html=True,
    )
