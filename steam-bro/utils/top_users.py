import helper , preprocessor
df = preprocessor.preprocess()
def top_users(st):
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