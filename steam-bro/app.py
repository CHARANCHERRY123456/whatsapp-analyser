import streamlit as st
import preprocessor , helper
import matplotlib.pyplot as plt


st.sidebar.title("QWhats app analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)
    st.dataframe(df)

    users_list = df["user"].unique().tolist()
    users_list.remove("notification")
    users_list.sort()
    users_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("show analysis for " , users_list)
    
    if st.sidebar.button("Show analysis"):
        messages_count , words , no_of_media_messages , no_of_links = helper.fetch_stats(selected_user , df)

        col1 , col2 , col3 , col4 = st.columns(4)

        with col2:
            st.header("Total Words")
            st.title(words)
        with col1:
            st.header("Total Messages")
            st.title(messages_count)
        with col3:
            st.header("Media Shared")
            st.title(no_of_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(no_of_links)
        
        # plot top busy users
        if selected_user == "Overall": # you can use use if you want group chats only
            st.title("Most Busy Users")
            buys_users , new_df = helper.most_busy_users(df)

            fig , ax = plt.subplots()
            col1 , col2 = st.columns(2)
            

            with col1:
                ax.bar(buys_users.index , buys_users.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        df_wc = helper.create_word_cloud(selected_user , df)
        fig , ax = plt.subplots()

        ax.imshow(df_wc)
        st.pyplot(fig)