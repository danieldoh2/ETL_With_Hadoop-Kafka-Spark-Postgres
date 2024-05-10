import sqlite3
import json
from confluent_kafka import Consumer


def create_database_and_table(db_name):
    """Create a new SQLite database and table if it does not already exist."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS health_events (
                      event_type TEXT,
                      timestamp TEXT,
                      location TEXT,
                      severity TEXT,
                      details TEXT
                    )''')

    connection.commit()
    connection.close()


def insert_health_event(connection, event_data):
    """Insert a health event into the SQLite database."""
    cursor = connection.cursor()

    # Extract the data fields
    event_type = event_data.get("EventType")
    timestamp = event_data.get("Timestamp")
    location = event_data.get("Location")
    severity = event_data.get("Severity")
    details = json.dumps(event_data.get("Details", {}))

    # Ensure all required fields are present
    if event_type and timestamp and location and severity:
        try:
            cursor.execute('''INSERT INTO health_events (event_type, timestamp, location, severity, details)
                              VALUES (?, ?, ?, ?, ?)''',
                           (event_type, timestamp, location, severity, details))
            connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error inserting data: {e}")
    else:
        print("Missing required fields in event data")


def basic_consume():
    # Configure Kafka consumer
    conf = {
        'bootstrap.servers': '44.201.154.178:9092',
        'group.id': 'my_consumer_group',
        'auto.offset.reset': 'latest'  # Start consuming from the latest offset of the topic
    }

    # Create Kafka consumer
    consumer = Consumer(conf)

    # Create a database and table
    db_name = 'health_data.db'
    create_database_and_table(db_name)

    # Connect to the SQLite database
    connection = sqlite3.connect(db_name)

    running = True
    try:
        consumer.subscribe(['health_events'])

        while running:
            msg = consumer.poll(timeout=10.0)
            if msg is None:
                continue
            elif msg.error():
                print(f"Kafka error: {msg.error()}")
                continue
            else:
                try:
                    message = msg.value().decode('utf-8')
                    data = json.loads(message)
                    insert_health_event(connection, data)
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error processing message: {e}")
    except Exception as e:
        print(e)
    finally:
        # Close Kafka consumer and SQLite connection
        consumer.close()
        connection.close()


if __name__ == "__main__":
    basic_consume()
