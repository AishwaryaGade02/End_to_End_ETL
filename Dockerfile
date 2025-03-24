FROM quay.io/astronomer/astro-runtime:12.7.1

RUN pip install --no-cache-dir \
    pandas \ 
    requests \
    pyspark \ 
    streamlit \
    plotly \
    transformers \ 
    nltk \
    sqlalchemy \
    psycopg2-binary \
    torch torchvision torchaudio \
    tf-keras\
    tensorflow


ENV PYSPARK_PYTHON=python3