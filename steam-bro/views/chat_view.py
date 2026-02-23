"""Chat view for RAG-based chat interface"""
import streamlit as st
import traceback

def render_chat_view(rag):
    """Render the chat view with RAG integration"""
    st.title("💬 Chat with Your WhatsApp Data")
    st.markdown("Ask questions about your chat history using AI!")
    
    # Display chat history in main area
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input in main area
    user_query = st.chat_input("Ask a question about your chat...")
    
    if user_query:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        # Get response from RAG
        try:
            with st.spinner("Thinking..."):
                answer = rag.ask_query(user_query)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()  # Rerun to show the new message
        except Exception as e:
            # Print error to console for debugging
            print(f"RAG Error: {str(e)}")
            traceback.print_exc()
            
            # Show detailed error to user
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()  # Rerun to show the error message
    
    # Clear chat button in sidebar
    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.sidebar.success("Chat history cleared!")
        st.rerun()
