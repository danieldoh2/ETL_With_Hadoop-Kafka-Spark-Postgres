import psycopg2
from confluent_kafka import Consumer, KafkaError
import json
import os
import time
import datetime

# Kafka Consumer Setup
conf = {
    'bootstrap.servers': '44.201.154.178:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf)
consumer.subscribe(['health_events'])

# PostgreSQL connection


def connect_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST"),
                database=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD")
            )
            print("Database connection established.")
            return conn
        except psycopg2.OperationalError as e:
            print("Database connection failed:", e)
            print("Retrying in 5 seconds...")
            time.sleep(5)

# Create Table


def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_events (
        id SERIAL PRIMARY KEY,
        details TEXT,
        location TEXT,
        severity TEXT,
        event_type TEXT,
        timestamp TIMESTAMP,
        severity_encoded INTEGER,
        date_only DATE
    );
    """)
    print("Table checked/created.")

# Map Severity to Code


def severity_to_code(severity):
    mapping = {'low': 1, 'medium': 2, 'high': 3}
    return mapping.get(severity.lower(), 0)

# Extract Date Function


def extract_date(timestamp):
    return datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").date()

# Process Individual Kafka Message


def process_message(msg, cursor):
    data = json.loads(msg.value().decode('utf-8'))
    severity_code = severity_to_code(data['Severity'])
    event_date = extract_date(data['Timestamp'])

    cursor.execute("""
        INSERT INTO health_events (details, location, severity, event_type, timestamp, severity_encoded, date_only)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
        data['Details'],
        data['Location'],
        data['Severity'],
        data['EventType'],
        data['Timestamp'],
        severity_code,
        event_date
    ))

# Process Messages


def consume_kafka_messages(consumer, cursor, conn):
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            try:
                process_message(msg, cursor)
                conn.commit()
            except Exception as e:
                print(f"Error processing message: {e}")
                conn.rollback()

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    conn = connect_db()
    cursor = conn.cursor()
    create_table(cursor)

    consume_kafka_messages(consumer, cursor, conn)
