from confluent_kafka import Consumer, KafkaError
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

Base = declarative_base()
# # Define the table structure


class GeneralHealthReport(Base):
    __tablename__ = 'general_health_reports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    location = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)
    details = Column(Text)


def sqlalchemy_connect():
    host = "localhost"
    database = "thedb"
    username = "postgres"
    password = "password123"
    port = "5432"
    try:
        connnection_str = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(connnection_str)
        Base.metadata.create_all(engine)
        print("success")
        # Session = sessionmaker(bind=engine)
        # session = Session()
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

        while running:
            msg = consumer.poll(timeout=10.0)
            if msg is None:
                continue
            else:
                message = msg.value().decode('utf-8')
                data = json.loads(message)
                # Insert the message into the database
                insert_general_health_report(session, data)
    except Exception as e:
        print(e)
    finally:
        consumer.close()
        # session.close()


def insert_general_health_report(session, event_data):
    try:
        new_report = GeneralHealthReport(
            event_type=event_data.get("EventType"),
            timestamp=event_data.get("Timestamp"),
            location=event_data.get("Location"),
            severity=event_data.get("Severity"),
            details=event_data.get("Details")
        )
        session.add(new_report)
        session.commit()
        print("Data inserted successfully")
    except Exception as e:
        session.rollback()
        print(f"Error inserting data: {e}")


if __name__ == '__main__':
    sqlalchemy_connect()
