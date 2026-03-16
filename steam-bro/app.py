"""Main Streamlit app for WhatsApp Chat Analyzer"""
import streamlit as st
import preprocessor
from utils.rag_utils import setup_rag
from views.analysis_view import render_analysis_view
from views.chat_view import render_chat_view
from utils.sidebar_utils import render_view_toggle
from cache_utils import save_chat_df, load_chat_df, list_cached_chats

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "view" not in st.session_state:
    st.session_state.view = "analysis"  # Default to analysis view

st.sidebar.title("Whats app analyser")

# Sidebar: file upload
uploaded_file = st.sidebar.file_uploader("Upload new chat")

# Sidebar: history of cached chats
cached_chats = list_cached_chats()
history_choice = st.sidebar.selectbox(
    "Or load a previous chat",
    ["Select"] + cached_chats,
)

df_active = None
rag_active = None
active_name = None

# Case 1: user uploaded a new file this session
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Save to cache using helper
    save_chat_df(uploaded_file.name, df)

    # Setup RAG for this chat
    rag = setup_rag(df, uploaded_file.name)

    df_active = df
    rag_active = rag
    active_name = uploaded_file.name

# Case 2: no new upload, but user picked from history
elif history_choice != "Select":
    df_hist = load_chat_df(history_choice)
    if df_hist is not None:
        df_active = df_hist
        rag_active = setup_rag(df_hist, history_choice)
        active_name = history_choice

# If we have an active chat, render the views
if df_active is not None:
    render_view_toggle()

    if st.session_state.view == "analysis":
        render_analysis_view(df_active)
    else:
        render_chat_view(rag_active)
