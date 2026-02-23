"""Main Streamlit app for WhatsApp Chat Analyzer"""
import streamlit as st
import preprocessor
from utils.rag_utils import setup_rag
from views.analysis_view import render_analysis_view
from views.chat_view import render_chat_view
from utils.sidebar_utils import render_view_toggle

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "view" not in st.session_state:
    st.session_state.view = "analysis"  # Default to analysis view

st.sidebar.title("Whats app analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # Read and preprocess file
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    # Setup RAG
    rag = setup_rag(df, uploaded_file.name)
    
    # Render view toggle buttons
    render_view_toggle()
    
    # Main content area - switch between views
    if st.session_state.view == "analysis":
        render_analysis_view(df)
    else:
        render_chat_view(rag)
