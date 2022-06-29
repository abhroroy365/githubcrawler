import streamlit as st
import pandas as pd
import numpy as np
from repo import scrap_repo
from topics import scrap_topics

st.markdown("<h1 style='text-align: center;'>Github Crawler</h1>", unsafe_allow_html=True)

# def make_clickable(link):
#     # target _blank to open new window
#     # extract clickable text to display for your link
#     text = link.split('=')[0]
#     return f'<a target="_blank" href="{link}">{text}</a>'

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

def display_repos(x,urls,topic):
    repo_df = scrap_repo(urls[x])
    # download button for repositories data
    csv = convert_df(repo_df)
    st.download_button(
        label="Save {} repositories as CSV".format(topic[x]),
        data=csv,
        file_name=str(topic[x])+'.csv',
        mime='text/csv',
    )
    # display repositories
    # repo_df['User Link'] = repo_df['User Link'].apply(make_clickable)
    # repo_df['Repository Link'] = repo_df['Repository Link'].apply(make_clickable)
    st.dataframe(repo_df)


def display_topics():
    number = 30
    with st.sidebar:
        agree = st.checkbox('Show more topics')
        if agree:
            number = st.radio(
                "Choose number of topics :",
                (30, 60, 90, 120, 150, 180)
            )
    df= scrap_topics(number)
  # download button for topic data
    csv = convert_df(df)
    st.download_button(
        label="Download topics as CSV",
        data=csv,
        file_name='trending_github_topics.csv',
        mime='text/csv',
    )
    user_table = df
    user_table['Repositories'] =''
    col = st.columns((1, 2, 2, 1, 1))
    st.write('Showing top {} topics out of 180 trending topics'.format(number))
    for x, topic in enumerate(user_table['topic']):
        col1, col2, col3, col4, col5 = st.columns((1, 2, 2, 1, 1))
        col1.write(x+1)  # index
        col2.write(user_table['topic'][x]) 
        col3.write(user_table['description'][x]) 
        col4.write(user_table['url'][x]) 
        show_repo = user_table['Repositories'][x]  # flexible type of button
        button_type = "Show Repositories"
        button_phold = col5.empty()  # create a placeholder
        do_action = button_phold.button(button_type, key=x)
        if do_action:
            button_phold.empty()
            with st.spinner("Loading..."):
                display_repos(x,user_table['url'],user_table['topic'])

    st.markdown("<br><h6 style='text-align: center; color: white;'>Developed by Abhra Ray Chaudhuri</h6>", unsafe_allow_html=True)
    

def main():
    st.markdown("<h4 style='text-align: center;'>What are the trending github topics currently ?</h4><br>", unsafe_allow_html=True)
    display_topics() 

if __name__ == '__main__':
    main()