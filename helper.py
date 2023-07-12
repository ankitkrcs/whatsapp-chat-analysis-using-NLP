from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extractor=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # fetch the number of messages
    num_messages = df.shape[0]
    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    # fetch the total number of media messages
    num_media_msg=df[df['message']=='<Media omitted>\n'].shape[0]

    links=[]
    for message in df['message']:
        
        links.extend(extractor.find_urls(message))
    return num_messages, len(words),num_media_msg,len(links)


def busy_user(df):
    x=df['user'].value_counts().head()
    new_df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(columns={'index': 'user', 'user': 'percent'})

    return x,new_df


def generate_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    word_cloud = WordCloud(width=500, height=300,min_font_size=10, max_words=100,background_color="white")
    df_wc=word_cloud.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_com_word(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_word=f.read()
    

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp=df[df['user'] != 'group_notification']
    temp=temp[temp['message'] != '<Media omitted>\n']
    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_word and len(word)>5:
               words.append(word)


    most_com=pd.DataFrame(Counter(words).most_common(20))
    return most_com
        


def emoji(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


#time analysis
def time_analysis(selected_user,df):
     if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
     time_analysis=df.groupby(['year','month_num','month']).count()['message'].reset_index()
     time=[]
     for i in range(time_analysis.shape[0]):
         time.append(time_analysis['month'][i]+'-'+str(time_analysis['year'][i]))
    
     time_analysis['time']=time

     return time_analysis

#Daily_Timeline
def daily_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    

    daily_timeline=df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline



def busy_day(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    busy_day=df['day_name'].value_counts()
    return busy_day


def monthly_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    monthly_analysis=df['month'].value_counts()
    return monthly_analysis


def het_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    activiy_heat_map=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activiy_heat_map