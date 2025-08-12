import streamlit as st
import preprocessor

st.sidebar.title("QWhats app analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)
    st.dataframe(df)

    users_list = df["user"].unique().tolist()
    users_list.remove("group notification")
    users_list.sort()
    users_list.insert(0,"Overall")
    st.sidebar.selectbox("show analysis for " , users_list)
    
    if st.sidebar.button("Show analysis"):
        pass