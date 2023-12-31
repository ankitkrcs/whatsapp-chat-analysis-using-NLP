import streamlit as st
import preprocessing
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    df=preprocessing.preprocess(data)
    # st.dataframe(df)


    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("Select User",user_list)

    if st.sidebar.button("Show Analysis"):
       num_messages,words,num_media_msg,links= helper.fetch_stats(selected_user,df)
       st.title("Statistics Overview")
       col1,col2,col3,col4=st.columns(4)
       
       with col1:
            st.header("Total Messages")
            st.title(num_messages)
       with col2:
            st.header("Total Words")
            st.title(words)
       with col3:
               st.header("Media Shared")
               st.title(num_media_msg)
       with col4:
               st.header("Links Shared")
               st.title(links)



               #timeline
    st.title("Monthly Timeline Analysis")
    time_analysis=helper.time_analysis(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(time_analysis['time'],time_analysis['message'],color='green')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    #daily timeline
    st.title("Daily Timeline Analysis")
    daily_analysis=helper.daily_analysis(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(daily_analysis['only_date'],daily_analysis['message'],color='green')
    plt.xticks(rotation=45)
    st.pyplot(fig)

     #activity map
    st.title("Activity Map")
    col1,col2=st.columns(2)
    
    with col1:
          st.title("Most Busy Day")
          busy_day=helper.busy_day(selected_user,df)
          fig,ax=plt.subplots()
          ax.bar(busy_day.index,busy_day.values, color='blue')
          st.pyplot(fig)
    with col2:
          st.title("Most Busy Month")
          busy_month=helper.monthly_analysis(selected_user,df)
          fig,ax=plt.subplots()
          ax.bar(busy_month.index,busy_month.values, color='yellow')
          plt.xticks(rotation="vertical")
          st.pyplot(fig)
     
          st.title("Weekly Activity Map")
          activity_heatmap=helper.het_map(selected_user,df)
          fig,ax=plt.subplots()
          ax=sns.heatmap(activity_heatmap)
          st.pyplot(fig)
   
     #find the busiest user
    if selected_user == 'Overall':
        st.title("Busiest User")
        x,new_df= helper.busy_user(df)
        fig,ax = plt.subplots()
          
        col1,col2=st.columns(2)
        with col1:
               ax.bar(x.index,x.values, color='green')
               plt.xticks(rotation=45)
               st.pyplot(fig)
        with col2:
               st.dataframe(new_df)

     #generate wordcloud
    st.title('word_cloud')
    df_wc= helper.generate_wordcloud(selected_user,df)
    fig,ax=plt.subplots()
    plt.imshow(df_wc)
    st.pyplot(fig)

    #most_common_word
    st.title('Most Common Words')
    most_com= helper.most_com_word(selected_user,df)
    fig,ax=plt.subplots()
    ax.barh(most_com[0],most_com[1], color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    emoji_df=helper.emoji(selected_user,df)
    st.dataframe(emoji_df)


    emoji_df=helper.emoji(selected_user,df)
    st.dataframe(emoji_df)
footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="#" target="_blank">©Ankit Maddheshiya</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
    

    
    
