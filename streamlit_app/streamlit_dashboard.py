import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

db_config = {
    "user": "postgres",
    "password": "postgres",
    "host": "postgres",  # Docker service name from docker-compose.yml
    "port": "5432",
    "database": "finance_db"
}

engine = create_engine(
    f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
)

st.title("Financial Data Dashboard")


tickers = ["AAPL","TSLA","GOOGL","AMZN","MSFT"]
ticker = st.selectbox("Select a Ticker Symbol",tickers)

# @st.cache_data
def fetch_stock_prices(ticker):
    query = f"SELECT * FROM stock_prices WHERE ticker='{ticker}' ORDER BY date DESC LIMIT 50"
    return pd.read_sql(query,engine)

# @st.cache_data
def fetch_news_sentiment():
    query = f"SELECT * FROM news_sentiment ORDER BY id DESC LIMIT 10"
    return pd.read_sql(query,engine)

stock_df = fetch_stock_prices(ticker)
news_df = fetch_news_sentiment()

if not stock_df.empty:
    st.subheader(f"Stock Price Trends for {ticker}")
    fig = px.line(stock_df, x="date", y="close", title=f"{ticker} Stock Prices")
    st.plotly_chart(fig)

else:
    st.warning(f"No stock data available for {ticker}.")

if not news_df.empty:
    st.subheader(f"Latest News Sentiment Analysis for {ticker}")
    st.dataframe(news_df[["title","sentiment"]])

else:
    st.warning(f"No news sentiment data available for {ticker}")