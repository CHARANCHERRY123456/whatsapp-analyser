"""Analysis view for WhatsApp chat analysis"""
import streamlit as st
import helper
import matplotlib.pyplot as plt

def render_analysis_view(df):
    """Render the analysis view with all charts and stats"""
    st.dataframe(df)

    # Fetching unique users
    users_list = df["user"].unique().tolist()
    users_list.remove("notification")
    users_list.sort()
    users_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("show analysis for ", users_list)
    
    if st.sidebar.button("Show analysis"):
        # Initial stats
        messages_count, words, no_of_media_messages, no_of_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

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

        # Monthly timeline
        st.title("Monthly time line")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["message"], color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline["only_date"], daily_timeline['message'], color="black")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # Activity map
        st.title("Activity map")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Finding the busiest user in group level
        if selected_user == 'Overall':
            st.title("Most busy user")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # WordCloud
        st.title("World Cloud")
        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # Plot most busy users
        if selected_user == "Overall":
            st.title("Most Busy Users")
            buys_users, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(buys_users.index, buys_users.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
