import psycopg2
from confluent_kafka import Consumer, KafkaError
<<<<<<< HEAD
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
        'auto.offset.reset': 'earliest'  # Start consuming from the latest offset of the topic
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
=======
import sqlalchemy as sql
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base
import json
from os import environ as env

Base = declarative_base()
# # Define the table structure


class GeneralHealthReport(Base):
    __tablename__ = 'general_health_reports'
    event_type = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    location = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)
>>>>>>> bfd8c7796a291538ec69867e8c4499d1adc3edf3

conn = connect_db()
cursor = conn.cursor()
create_table(cursor)

<<<<<<< HEAD
def severity_to_code(severity):
    mapping = {'low': 1, 'medium': 2, 'high': 3}
    return mapping.get(severity.lower(), 0)  # default to 0 if unknown

def extract_date(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").date()
=======
def create_db_engine() -> sql.engine.base.Engine:
    """Create and return a SQLAlchemy database engine.

    Returns:
    sql.engine.base.Engine: The database engine.
    """
    db_url = sql.URL.create(
        drivername="postgresql",
        username="postgres",
        password="pass",
        host="localhost",
        database="thedb",
    )
    return sql.create_engine(db_url)


def create_db_session(engine: sql.engine.base.Engine) -> sessionmaker[Session]:
    """Create and return a SQLAlchemy database session.

    Parameters:
    engine (sql.engine.base.Engine): The database engine to use.

    Returns:
    sql.orm.session.Session: The database session.
    """
    session_factory = sessionmaker(bind=engine)
    return session_factory()


def sqlalchemy_connect():
    host = ""
    database = "thedb"
    username = "postgres"
    password = "password123"
    port = "5432"
    try:
        connnection_str = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(connnection_str)
        Base.metadata.create_all(engine)
        print("success")
        Session = sessionmaker(bind=engine)
        session = Session()
    except Exception as e:
        print(e)


def basic_consume():
    # Configure Kafka consumer
    conf = {
        'bootstrap.servers': '44.201.154.178:9092',
        'group.id': 'my_consumer_group',
        'auto.offset.reset': 'latest'  # Start consuming from the latest offset of the topic
    }

    # Create Kafka consumer
    consumer = Consumer(conf)

    running = True
    try:
        consumer.subscribe(['health_events'])

        consumer.poll(0)
>>>>>>> bfd8c7796a291538ec69867e8c4499d1adc3edf3

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
<<<<<<< HEAD
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
=======
                message = msg.value().decode('utf-8')
                data = json.loads(message)
                # Insert the message into the database
                # insert_general_health_report(session, data)
    except Exception as e:
        print(e)
    finally:
        consumer.close()
        # session.close()


# def insert_general_health_report(session, event_data):
#     try:
#         new_report = GeneralHealthReport(
#             event_type=event_data.get("EventType"),
#             timestamp=event_data.get("Timestamp"),
#             location=event_data.get("Location"),
#             severity=event_data.get("Severity"),
#             details=event_data.get("Details")
#         )
#         session.add(new_report)
#         session.commit()
#         print("Data inserted successfully")
#     except Exception as e:
#         session.rollback()
#         print(f"Error inserting data: {e}")
>>>>>>> bfd8c7796a291538ec69867e8c4499d1adc3edf3

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
    cursor.close()
    conn.close()

<<<<<<< HEAD
=======
if __name__ == '__main__':
    sqlalchemy_connect()
>>>>>>> bfd8c7796a291538ec69867e8c4499d1adc3edf3
