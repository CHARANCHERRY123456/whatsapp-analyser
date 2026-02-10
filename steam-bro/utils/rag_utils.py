"""RAG initialization utilities"""
import streamlit as st
from rag_src.main import RAG

@st.cache_resource
def initialize_rag(df):
    """Initialize RAG system from dataframe"""
    data = list(zip(df["user"].to_list(), df["message"].to_list(), df["date"].to_list()))
    return RAG(data)

def setup_rag(df, uploaded_file_name):
    """Setup and cache RAG in session state"""
    if "rag" not in st.session_state or st.session_state.get("rag_file") != uploaded_file_name:
        with st.spinner("Initializing RAG system..."):
            st.session_state.rag = initialize_rag(df)
            st.session_state.rag_file = uploaded_file_name
        st.success("✅ RAG system ready!")
    else:
        st.info("✅ RAG system ready!")
    
    return st.session_state.rag
