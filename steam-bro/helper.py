from urlextract import URLExtract
from wordcloud import WordCloud

extract = URLExtract()

def fetch_stats(user , df):
    if user != "Overall":
        df = df[df["user"]  == user]
    # shape[0] gives number of rows means no fo messages
    num_messages =  df.shape[0]
    words = []
    for message in df["message"]:
        words.extend(message.split())
    
    # we can able to match if it was ending with (file attached) this will be used in when extracgted with media
    no_of_media_messages = df[df["message"] == "<Media omitted>\n" ].shape[0]


    # no of links shared
    links = []
    for message in df["message"]:
        links.extend(extract.find_urls(message))

    return (num_messages , len(words) , no_of_media_messages , len(links))



def most_busy_users(df):
    top_users_df = df["user"].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns={'index': "name", "user": "percentage"}
    )
    return top_users_df , df

def create_word_cloud(user , df):
    if user != "Overall":
        df = df[df["user"] == user]
    
    not_words = set("<Media omitted>\n")
    
    wc = WordCloud(width=500 , height=500 , min_font_size=10 , background_color='white')
    df = df[df["message"] not in not_words]
    df_wc = wc.generate(df["message"].str.cat(sep=" "))
    return df_wc