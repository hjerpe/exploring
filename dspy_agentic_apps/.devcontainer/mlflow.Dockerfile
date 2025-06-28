FROM ghcr.io/mlflow/mlflow:latest
RUN pip install --no-cache-dir psycopg2-binary==2.9.9 boto3==1.34.126
