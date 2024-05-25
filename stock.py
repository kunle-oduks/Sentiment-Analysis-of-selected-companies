

import pandas as pd
import numpy as np
import nltk
from bs4 import BeautifulSoup
from datetime import datetime
import streamlit as st
from urllib.request import Request, urlopen
import matplotlib.pyplot as plt
import plotly.express as px

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

st.markdown("<h1 style = 'color: #0C2D57; text-align: center; font-size: 60px; font-family: Helvetica'>SENTIMENT ANALYSIS OF SELECTED COMPANIES</h1>", unsafe_allow_html = True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h4 style = 'margin: -30px; color: #F11A7B; text-align: center; font-family: cursive '>Built By Kunle Odukoya</h4>", unsafe_allow_html = True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3, = st.columns(3)

c2.image('pngwing.com (20).png', width = 400)

company = ['AAPL', 'AMZN', 'GOOG', 'TSLA', 'MSFT', 'META', 'XOM', 'CVX', 'NFLX']

st.sidebar.image('pngwing.com (21).png')
st.markdown("<br>", unsafe_allow_html=True)
user_input = st.sidebar.selectbox("Choose the company's ticker", options = company)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

url = f'https://finviz.com/quote.ashx?t={user_input}'
req = Request(url=url, headers={'user-agent': 'my-app'})
response = urlopen(req)

html = BeautifulSoup(response, 'html')
df= pd.DataFrame(columns= ['Date', 'Time', 'Title'])
news_table = html.find('table', id = 'news-table')
rows = news_table.find_all('tr')
for row in rows:
    #link = row.a.get('href')
    title = row.a.text.strip()
    Date_data = row.td.text.strip().split(' ')

    if len(Date_data) == 1:
        time = Date_data[0]
    else:
        if Date_data[0] == 'Today':
            today = datetime.today().date()
            date = today.strftime('%m-%d-%y')
            time = Date_data[1]
        else:
            date = Date_data[0]
            time = Date_data[1]
    
    the_row = [date, time, title]
    l = len(df)
    df.loc[l]= the_row

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.subheader(f'News Table for {user_input} ', divider = True)
st.dataframe(df, use_container_width = True)

df['Date'] = pd.to_datetime(df['Date']).dt.date

vader = SentimentIntensityAnalyzer()
df_analysed = pd.DataFrame()
df_analysed['Date'] = df['Date']
df_analysed['Time'] = df['Time']
df_analysed['Title'] = df['Title']
df_analysed['Score'] = df['Title'].apply(lambda x: vader.polarity_scores(x)['compound'])

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.subheader(f'Compound Polarity Score for {user_input} ', divider = True)
st.dataframe(df_analysed, use_container_width = True)

mean_df = df_analysed.groupby('Date')['Score'].mean()
#mean_df = mean_df.unstack()
mean_df = mean_df.transpose()
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

def plot_line():
    fig = px.line(data_frame=df_analysed, x= 'Time', y = 'Score')
    c1.plotly_chart(fig)

def plot_bar():
    fig = px.bar(data_frame=df_analysed, x= 'Date', y = 'Score')
    c1.plotly_chart(fig)

st.sidebar.button('Time Chart', on_click = plot_line)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.sidebar.button('Daily Chart', on_click = plot_bar)






