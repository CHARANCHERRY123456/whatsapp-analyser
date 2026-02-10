"""Sidebar utilities for view toggling"""
import streamlit as st

def render_view_toggle():
    """Render view toggle buttons in sidebar"""
    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("📊 Analysis", use_container_width=True):
            st.session_state.view = "analysis"
            st.rerun()
    with col2:
        if st.button("💬 Chat", use_container_width=True):
            st.session_state.view = "chat"
            st.rerun()
    
    # Show current view indicator
    if st.session_state.view == "analysis":
        st.sidebar.success("📊 Analysis View")
    else:
        st.sidebar.success("💬 Chat View")
