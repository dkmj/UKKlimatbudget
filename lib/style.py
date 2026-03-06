"""Shared styling — background image and color palette from Flower Wild photo."""

import base64
from pathlib import Path

import streamlit as st

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

        /* Hide sidebar navigation entirely (replaced by nav-bar) */
        [data-testid="stSidebarNav"] {{
            display: none !important;
        }}

        /* --- Hub cards (glassmorphic) --- */
        .hub-card {{
            background: rgba(45, 27, 78, 0.55);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(91, 45, 142, 0.4);
            border-radius: 12px;
            padding: 1.25rem 1rem;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.25s, border-color 0.25s;
            min-height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        .hub-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 28px rgba(0, 0, 0, 0.35),
                        0 0 20px var(--accent-color, rgba(123, 45, 142, 0.3));
            border-color: var(--accent-color, {PALETTE["magenta"]});
        }}
        .hub-card .hub-icon {{
            font-size: 2rem;
            margin-bottom: 0.3rem;
        }}
        .hub-card .hub-title {{
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: {PALETTE["white"]} !important;
            margin: 0.25rem 0 !important;
        }}
        .hub-card .hub-desc {{
            font-size: 0.8rem !important;
            color: {PALETTE["cream"]} !important;
            opacity: 0.85;
            margin: 0 !important;
        }}

        /* --- Nav bar (compact icon row on sub-pages) --- */
        .nav-item {{
            text-align: center;
            padding: 0.4rem 0.25rem;
            border-radius: 8px;
            font-size: 0.8rem;
            color: {PALETTE["cream"]};
            line-height: 1.3;
        }}
        .nav-item.active {{
            background: rgba(91, 45, 142, 0.4);
            border: 1px solid {PALETTE["magenta"]};
            box-shadow: 0 0 10px rgba(123, 45, 142, 0.3);
        }}
        .nav-item .nav-label {{
            font-size: 0.65rem;
            opacity: 0.9;
        }}

        /* --- Format bar (multi-format signal) --- */
        .format-bar {{
            display: inline-flex;
            gap: 0.75rem;
            background: rgba(45, 27, 78, 0.5);
            border: 1px solid rgba(91, 45, 142, 0.3);
            border-radius: 20px;
            padding: 0.35rem 1rem;
            font-size: 0.8rem;
            color: {PALETTE["cream"]};
            margin-bottom: 1rem;
        }}
        .format-bar span {{
            opacity: 0.85;
        }}

        /* --- Hub hero --- */
        .hub-hero {{
            text-align: center;
            padding: 1rem 0 0.5rem;
        }}
        .hub-hero h1 {{
            font-size: 2.2rem !important;
            margin-bottom: 0.25rem !important;
        }}
        .hub-tagline {{
            font-size: 1.1rem !important;
            color: {PALETTE["gold"]} !important;
            opacity: 0.9;
            margin-bottom: 1rem !important;
        }}

        /* Responsive — mobile cards */
        @media (max-width: 768px) {{
            .hub-card {{
                padding: 0.75rem;
                min-height: 120px;
            }}
            .hub-card .hub-icon {{
                font-size: 1.5rem;
            }}
        }}

        /* Sidebar linkroll — match Streamlit nav item styling */
        .sidebar-linkroll .linkroll-heading {{
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: {PALETTE["cream"]} !important;
            opacity: 0.55;
            margin-bottom: 0.25rem !important;
            padding-left: 0.5rem;
        }}
        .sidebar-linkroll a {{
            display: block !important;
            padding: 0.375rem 0.5rem !important;
            border-radius: 0.375rem !important;
            font-size: 0.875rem !important;
            font-weight: 400 !important;
            color: {PALETTE["cream"]} !important;
            text-decoration: none !important;
            transition: background 0.15s, color 0.15s;
        }}
        .sidebar-linkroll a:hover {{
            background: rgba(91, 45, 142, 0.35) !important;
            color: {PALETTE["white"]} !important;
        }}
        .sidebar-linkroll a::after {{
            content: " ↗";
            font-size: 0.7em;
            opacity: 0.5;
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
