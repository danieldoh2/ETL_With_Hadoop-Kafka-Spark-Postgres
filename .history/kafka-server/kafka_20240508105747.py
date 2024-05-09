from confluent_kafka import Consumer, KafkaError
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Define the table structure
# class EmergencyIncident(Base):
#     __tablename__ = 'emergency_incidents'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     incident_type = Column(String(100), nullable=False)
#     location = Column(String(255), nullable=False)
#     description = Column(Text, nullable=True)
#     reported_at = Column(TIMESTAMP, server_default=func.now())

# def sqlalchemy_connect():
#     host = "localhost"
#     database = "thedb"
#     username = "postgres"
#     password = "password123"
#     port = "5432"
#     try:
#         connnection_str = f"postgresql://{username}:{password}@{host}:{port}/{database}"
#         engine = create_engine(connnection_str)
#         Base = declarative_base()
#         Session = sessionmaker(bind=engine)
#         session = Session()
#     except Exception as e:
# print(e)


def basic_consume(consumer):
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
        consumer.subscribe(['health_event'])

        consumer.poll(0)

        while running:
            msg = consumer.poll(timeout=10.0)
            if msg is None:
                continue
            else:
                message = msg.value().decode('utf-8')
                print(message)
                print(type(message))
                # print('Received message: {}'.format(
                #     msg.value().decode('utf-8')))
    except Exception as e:
        print(e)
    finally:
        consumer.close()


if __name__ == '__main__':
    # sqlalchemy_connect()
    basic_consume(consumer)
