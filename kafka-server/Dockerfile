FROM docker.io/bitnami/kafka:3.7

FROM python:3.8-slim

# Install pip if not available (unlikely necessary but a safeguard)
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

# Install necessary Python packages
RUN pip install --no-cache-dir confluent_kafka psycopg2-binary

# Copy your Python script to the container
COPY ./kafka.py /app/kafka.py

# Set the command to run your application
CMD ["python", "/app/kafka.py"]