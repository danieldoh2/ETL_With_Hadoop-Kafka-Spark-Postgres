from confluent_kafka import Consumer, KafkaError
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

# Define the Base class and table structure
Base = declarative_base()


class GeneralHealthReport(Base):
    __tablename__ = 'general_health_reports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    location = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)
    details = Column(Text)

# Connect to the PostgreSQL database and create the table


def sqlalchemy_connect():
    host = "localhost"
    database = "thedb"
    username = "postgres"
    password = "password123"
    port = "5432"

    try:
        connection_str = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(connection_str)
        # Create the table if it doesn't already exist
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")

# Insert a record into the database


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

# Kafka Consumer to read messages from a topic and store them in the database


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
        # Subscribe to the desired Kafka topic
        consumer.subscribe(['health_events'])

        # Create a session for database interaction
        Session = sqlalchemy_connect()
        if not Session:
            print("Unable to create SQLAlchemy session")
            return
        session = Session()

        while running:
            msg = consumer.poll(timeout=10.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print('End of partition reached {0}/{1}'
                          .format(msg.topic(), msg.partition()))
                else:
                    print('Error: {0}'.format(msg.error()))
                    running = False
            else:
                # Process the Kafka message
                message = msg.value().decode('utf-8')
                print(f"Received message: {message}")
                data = json.loads(message)

                # Insert the message into the database
                insert_general_health_report(session, data)

    except Exception as e:
        print(f"Error in consumer: {e}")
    finally:
        consumer.close()
        session.close()


if __name__ == '__main__':
    basic_consume()
