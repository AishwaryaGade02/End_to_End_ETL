from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import requests
import json
import pandas as pd
from transformers import pipeline

POSTGRES_CONN_ID = 'postgres_default'
ALPHA_VANTAGE_API_CONN_ID = 'alpha_vantage_api'
NEWS_API_CONN_ID = 'news_api'

default_args = {
    'owner' : 'airflow',
    'start_date' : days_ago(1),
    'retries' : 1,
}

TICKERS = ["AAPL","TSLA","GOOGL","AMZN","MSFT"]

with DAG(dag_id='finance_etl_pipeline',
         default_args=default_args,
         schedule_interval='0 0 * * 1',
         catchup=False) as dag:
    
    @task()
    def extract_stock_data(ticker: str):
        http_hook = HttpHook(http_conn_id=ALPHA_VANTAGE_API_CONN_ID,method='GET')
        response = http_hook.run(f'/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey=1H1158KAOL8354HJ')
        data = response.json().get('Time Series (Daily)', {})

        if not data:
            raise ValueError("No stock data received from API.")
        
        df = pd.DataFrame(data).T.reset_index()
        df.columns = ["date","open","high","low","close","volume"]
        df["ticker"] = ticker

        return df.values.tolist()
    
    @task()
    def extract_news_sentiment(ticker: str):
        http_hook = HttpHook(http_conn_id = NEWS_API_CONN_ID, method='GET')
        response = http_hook.run(f'/v2/everything?q={ticker}&apiKey=6bd48dee9c0e438a86ebced4fdc74922')
        articles = response.json().get('articles',[])

        if not articles:
            raise ValueError("No articles received from API")
        
        news_df = pd.DataFrame(articles)[["title","content"]]
        sentiment_model = pipeline("sentiment-analysis",model="ProsusAI/finbert")
        news_df['sentiment'] = news_df['content'].apply(
            lambda x: sentiment_model(x[:200])[0]['label'] if pd.notnull(x) else 'neutral'
        )

        return news_df.values.tolist()
    
    @task()
    def load_data_to_postgres(stock_data_list,news_data_list):
        postgres_hook = PostgresHook(postgres_conn_id = POSTGRES_CONN_ID)
        conn = postgres_hook.get_conn()
        cursor = conn.cursor()
    
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS stock_prices (
                    id SERIAL PRIMARY KEY,
                    date DATE,
                    open FLOAT,
                    high FLOAT,
                    low FLOAT,
                    close FLOAT,
                    volume INT,
                    ticker VARCHAR(10)                        
                );    
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_sentiment(
                       id SERIAL PRIMARY KEY,
                       title TEXT,
                       content TEXT,
                       sentiment VARCHAR(50)
                       
                );    
        """)

        stock_insert_query = """
        INSERT INTO stock_prices(date, open, high, low, close, volume, ticker)
        VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;
        """

        news_insert_query = """
        INSERT INTO news_sentiment(title, content, sentiment)
        VALUES (%s,%s,%s) ON CONFLICT DO NOTHING;
        """
        for stock_data in stock_data_list:
            cursor.executemany(stock_insert_query,stock_data)
        for news_data in news_data_list:
            cursor.executemany(news_insert_query, news_data)

        conn.commit()
        cursor.close()

    stock_data_results = []
    news_data_results = []

    for ticker in TICKERS:
        stock_data_results.append(extract_stock_data(ticker)) 
        news_data_results.append(extract_news_sentiment(ticker))

    # ticker_symbol = "AAPL"
    # stock_data = extract_stock_data(ticker_symbol)
    # news_data = extract_news_sentiment(ticker_symbol)
    load_data_to_postgres(stock_data_results,news_data_results)

        