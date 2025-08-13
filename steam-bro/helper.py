from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd

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
    df = df[df["message"] != "<Media omitted>\n"]
    df_wc = wc.generate(df["message"].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    import os
    path = os.path.join(os.path.dirname(__file__), "stop_words_list.txt")
    f = open(path, "r",encoding="utf-8")
    stop_words = f.read()
    # f=open('stop_words_list.txt','r')
    # stop_words = f.read()

    if(selected_user != 'Overall'):
        df= df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'notification']
    temp=temp[temp['message'] != '<Media omitted>\n']

    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    return_df=pd.DataFrame(Counter(words).most_common(20))
    return return_df