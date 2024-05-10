from confluent_kafka import Consumer, KafkaError
import psycopg2

# Configure Kafka consumer
conf = {
    'bootstrap.servers': '44.201.154.178:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'latest'  # Start consuming from the latest offset of the topic
}

# Create Kafka consumer
consumer = Consumer(conf)

running = True


def connection_postgres():
    try:
        connection = psycopg2.connect(
            database="mydb", user="danield", password="bingbong300")
        print("success")
    except Exception as e:
        print(e)


def basic_consume(consumer):
    try:
        consumer.subscribe(['emergency_incident'])

        consumer.poll(0)

        while running:
            msg = consumer.poll(timeout=10.0)
            if msg is None:
                continue
            else:
                print('Received message: {}'.format(
                    msg.value().decode('utf-8')))
    except Exception as e:
        print(e)
    finally:
        consumer.close()


if __name__ == '__main__':
    connection_postgres()
    # basic_consume(consumer)
