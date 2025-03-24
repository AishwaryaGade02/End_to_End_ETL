# Use official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy Streamlit app files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir \
    streamlit pandas plotly sqlalchemy psycopg2-binary

# Expose the default Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
