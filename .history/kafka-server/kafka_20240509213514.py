import psycopg2
from confluent_kafka import Consumer, KafkaError
import json
import os
import time
import datetime
print("Environment Variables:")
print("POSTGRES_HOST:", os.getenv("POSTGRES_HOST"))
print("POSTGRES_USER:", os.getenv("POSTGRES_USER"))
print("POSTGRES_PASSWORD:", os.getenv("POSTGRES_PASSWORD"))
print("POSTGRES_DB:", os.getenv("POSTGRES_DB"))

# Kafka Consumer Setup
conf = {
    'bootstrap.servers': '44.201.154.178:9092',
    'group.id': 'my_consumer_group',
    # Start consuming from the latest offset of the topic
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

# def create_table(cursor):
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS health_events (
#             id SERIAL PRIMARY KEY,
#             json_column JSONB NOT NULL
#         );
#     """)
#     print("Table checked/created.")


def create_table(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS health_events (
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


conn = connect_db()
cursor = conn.cursor()
create_table(cursor)


def severity_to_code(severity):
    mapping = {'low': 1, 'medium': 2, 'high': 3}
    return mapping.get(severity.lower(), 0)  # default to 0 if unknown


def extract_date(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").date()


# Process messages
# try:
#     while True:
#         msg = consumer.poll(timeout=1.0)
#         if msg is None: continue
#         if msg.error():
#             if msg.error().code() == KafkaError._PARTITION_EOF:
#                 continue
#             else:
#                 print(msg.error())
#                 break
#         data = json.loads(msg.value().decode('utf-8'))
#         # Process and insert data into PostgreSQL
#         cursor.execute("INSERT INTO  health_events (json_column) VALUES (%s)", [json.dumps(data)])
#         conn.commit()
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

        data = json.loads(msg.value().decode('utf-8'))

        # Process and insert data into PostgreSQL
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
        conn.commit()

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
    cursor.close()
    conn.close()
