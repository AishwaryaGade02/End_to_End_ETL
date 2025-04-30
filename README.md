# 🛠️ End-to-End ETL Pipeline: Financial News & Stock Analytics

This project demonstrates a production-ready **End-to-End ETL pipeline** that ingests financial stock data and related news sentiment, processes it through scheduled pipelines, and visualizes key insights using interactive dashboards.

---

## 📌 Project Objectives

- Automate extraction of **stock prices** and **financial news sentiment** using public APIs.
- Transform and clean raw data into analytics-ready format.
- Load processed data into a PostgreSQL database.
- Schedule pipelines with **Apache Airflow** for regular data updates.
- Visualize insights using an interactive **Streamlit dashboard**.

---

## 🧰 Tech Stack

- **Languages**: Python (pandas, requests, SQLAlchemy, BeautifulSoup)
- **APIs**: Alpha Vantage API, NewsAPI
- **Data Orchestration**: Apache Airflow
- **Database**: PostgreSQL
- **Dashboard**: Streamlit
- **Containerization**: Docker

---

## ⚙️ Pipeline Overview

[API Ingestion] → [Data Cleaning & Transformation] → [PostgreSQL Storage] → [Streamlit Visualization] ↑ [Scheduled via Airflow]

## ▶️ Getting Started

Follow the steps below to run the full end-to-end ETL pipeline locally:

---

### 📁 1. Clone the Repository

```bash
git clone https://github.com/your-repo/End_to_End_ETL.git
cd End_to_End_ETL
```
### 🛰️ 2. Start Airflow via Astronomer CLI

Use the Astronomer CLI to launch the Airflow environment and trigger the DAG.

```bash
astro dev start
```
Access the **Airflow UI** at: [http://localhost:8080](http://localhost:8080)

### 📊 3. Run the Streamlit Dashboard

Once the ETL process completes, launch the dashboard to visualize insights.

```bash

docker-compose up streamlit  .
```
Access the **Streamlit Dashboard** at: [http://localhost:8501](http://localhost:8501)

