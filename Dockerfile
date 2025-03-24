# Use Astronomer Runtime as the base image
FROM quay.io/astronomer/astro-runtime:12.7.1

# Optional Spark environment
ENV PYSPARK_PYTHON=python3

# Expose Airflow webserver port
EXPOSE 8080

# Use "airflow standalone" as default command (optional)
CMD ["airflow", "standalone"]
