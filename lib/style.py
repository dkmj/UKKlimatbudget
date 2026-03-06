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

        /* Hide the default "app" page label in sidebar navigation */
        [data-testid="stSidebarNav"] li:first-child {{
            display: none !important;
        }}

        /* ===== Bageriet Redesign Styles ===== */
        
        /* completely hide the sidebar and its toggle button */
        [data-testid="stSidebar"] {{
            display: none !important;
        }}
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}
        
        /* Top Navigation Container */
        .top-nav-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(45, 27, 78, 0.65);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(123, 45, 142, 0.3);
            border-radius: 12px;
            padding: 8px 16px;
            margin-bottom: 24px;
            gap: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }}
        
        /* Hide Hook Containers */
        .element-container:has(.nav-item-wrapper),
        .element-container:has(.glass-card-wrapper) {{
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            margin-bottom: -1rem !important;
        }}
        
        /* Nav Item Styles applied to next st.page_link element */
        .element-container:has(.nav-item-wrapper) + .element-container a[data-testid="stPageLink-NavLink"] {{
            text-align: center;
            border-radius: 8px;
            transition: all 0.3s ease;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 4px !important;
            padding: 8px 12px !important;
            text-decoration: none !important;
            background: transparent !important;
        }}
        
        .element-container:has(.nav-item-wrapper) + .element-container a[data-testid="stPageLink-NavLink"]:hover {{
            background: rgba(123, 45, 142, 0.5) !important;
            transform: translateY(-2px);
        }}
        
        .element-container:has(.nav-item-wrapper) + .element-container a[data-testid="stPageLink-NavLink"] p {{
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            color: #E8E0D8 !important;
            margin: 0 !important;
        }}
        
        /* Default st header styling inner p element overrider */
        .element-container:has(.nav-item-wrapper) + .element-container a[data-testid="stPageLink-NavLink"] p > span {{
            font-size: 1.2rem;
        }}
        
        .element-container:has(.nav-item-wrapper.active-nav-item) + .element-container a[data-testid="stPageLink-NavLink"] {{
            background: rgba(217, 79, 122, 0.4) !important;
            box-shadow: 0 0 10px rgba(217, 79, 122, 0.6);
            border: 1px solid #D94F7A;
        }}
        
        /* Glass Cards for the hub applied to next st.page_link */
        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"] {{
            background: rgba(45, 27, 78, 0.5) !important;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(123, 45, 142, 0.4) !important;
            border-radius: 16px !important;
            padding: 24px !important;
            text-align: center;
            transition: all 0.3s ease;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            height: 180px !important; /* Fixed height to create a card shape since block text is outside */
            text-decoration: none !important;
        }}
        
        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"]:hover {{
            background: rgba(91, 45, 142, 0.7) !important;
            border-color: {PALETTE["pink"]} !important;
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3), 0 0 15px rgba(217, 79, 122, 0.4);
            cursor: pointer;
        }}
        
        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"] p {{
            font-size: 1.2rem !important;
            font-weight: bold !important;
            color: #F0EDE8 !important;
            margin: 0 !important;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }}
        
        /* Increase icon size dynamically */
        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"] p > span:first-child {{
            font-size: 2.5rem !important;
            line-height: 1;
        }}

        /* Inject descriptions manually via CSS depending on href */
        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"][href$="1_%C3%96versikt.py"]::after,
        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"][href$="1_\\00D6versikt.py"]::after {{
            content: "Dashboard med nyckeltal";
            display: block;
            font-size: 0.9rem !important;
            font-weight: normal !important;
            opacity: 0.8;
            color: #F0EDE8 !important;
            margin-top: -12px;
        }}

        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"][href$="2_Utforska.py"]::after {{
            content: "Sök och filtrera 72 åtgärder";
            display: block;
            font-size: 0.9rem !important;
            font-weight: normal !important;
            opacity: 0.8;
            color: #F0EDE8 !important;
            margin-top: -12px;
        }}

        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"][href$="3_Quiz.py"]::after {{
            content: "Testa din kunskap";
            display: block;
            font-size: 0.9rem !important;
            font-weight: normal !important;
            opacity: 0.8;
            color: #F0EDE8 !important;
            margin-top: -12px;
        }}

        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"][href$="4_Podcast.py"]::after {{
            content: "Lyssna 🎧 eller Läs 📖";
            display: block;
            font-size: 0.9rem !important;
            font-weight: normal !important;
            opacity: 0.8;
            color: #F0EDE8 !important;
            margin-top: -12px;
        }}

        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"][href$="5_Presentation.py"]::after {{
            content: "Bildspel för möten";
            display: block;
            font-size: 0.9rem !important;
            font-weight: normal !important;
            opacity: 0.8;
            color: #F0EDE8 !important;
            margin-top: -12px;
        }}

        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"][href$="6_Chatt.py"]::after {{
            content: "Ställ frågor om klimatbudgeten m h a AI";
            display: block;
            font-size: 0.9rem !important;
            font-weight: normal !important;
            opacity: 0.8;
            color: #F0EDE8 !important;
            margin-top: -12px;
        }}

        .element-container:has(.glass-card-wrapper) + .element-container a[data-testid="stPageLink-NavLink"][href$="7_Rapport.py"]::after {{
            content: "PDF 📄 eller Webb 🌐";
            display: block;
            font-size: 0.9rem !important;
            font-weight: normal !important;
            opacity: 0.8;
            color: #F0EDE8 !important;
            margin-top: -12px;
        }}
        
        .glass-card p {{
            font-size: 0.9rem !important;
            opacity: 0.8;
            margin-bottom: 0 !important;
        }}
        
        .glass-card .icon {{
            font-size: 2.5rem;
            margin-bottom: 8px;
        }}
        
        /* Hub Hero Section */
        .hub-hero {{
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 30px;
        }}
        
        .hub-hero h1 {{
            font-size: 2.5rem !important;
            margin-bottom: 10px !important;
            background: linear-gradient(90deg, {PALETTE["white"]}, {PALETTE["gold"]});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .hub-hero p {{
            font-size: 1.2rem !important;
            color: {PALETTE["cream"]} !important;
            max-width: 600px;
            margin: 0 auto !important;
        }}
        
        /* Adjust main padding since sidebar is gone */
        [data-testid="stMainBlockContainer"] {{
            padding-top: 2rem !important;
            max-width: 1000px !important;
        }}
        
        /* Footer linkroll */
        .footer-linkroll {{
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid rgba(123, 45, 142, 0.3);
            text-align: center;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }}
        
        .footer-linkroll a {{
            color: {PALETTE["cream"]} !important;
            text-decoration: none !important;
            font-size: 0.9rem;
            opacity: 0.7;
            transition: all 0.2s ease;
        }}
        
        .footer-linkroll a:hover {{
            opacity: 1;
            color: {PALETTE["pink"]} !important;
        }}
        
        /* Format tabs (Podcast/Rapport) */
        .format-tabs {{
            margin-bottom: 20px;
        }}
        </style>

        <div class="photo-credit">📷 C.Schubert</div>
        """,
        unsafe_allow_html=True,
    )
