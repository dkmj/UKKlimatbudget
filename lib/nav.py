"""Navigation components for the application."""
import streamlit as st


def render_top_nav(current_page: str = None):
    """
    Renders a compact horizontal top navigation bar replacing the sidebar.

    Args:
        current_page: The name of the current active page (e.g., "översikt").
    """
    st.markdown('<div class="top-nav-container">', unsafe_allow_html=True)
    
    # Define navigation items: (icon, label, page target)
    nav_items = [
        ("🌍", "Hem", "app.py"),
        ("📊", "Översikt", "pages/1_Översikt.py"),
        ("🔍", "Utforska", "pages/2_Utforska.py"),
        ("❓", "Quiz", "pages/3_Quiz.py"),
        ("🎙️", "Podcast", "pages/4_Podcast.py"),
        ("📑", "Presentation", "pages/5_Presentation.py"),
        ("💬", "Chatt", "pages/6_Chatt.py"),
        ("📄", "Rapport", "pages/7_Rapport.py")
    ]
    
    # Create columns for the navigation icons
    cols = st.columns(len(nav_items))
    
    for i, (icon, label, target) in enumerate(nav_items):
        with cols[i]:
            # Determine if this tab is active purely for styling purposes
            # The actual target page name should match standard conventions
            is_active = False
            if current_page:
                target_filename = target.split("/")[-1].split(".")[0].lower()
                is_active = current_page.lower() in target_filename
                
            active_class = 'active-nav-item' if is_active else ''
            
            st.markdown(f'<div class="nav-item-wrapper {active_class}">', unsafe_allow_html=True)
            st.page_link(target, label=label, icon=icon)
            st.markdown('</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-separator"></div>', unsafe_allow_html=True)
