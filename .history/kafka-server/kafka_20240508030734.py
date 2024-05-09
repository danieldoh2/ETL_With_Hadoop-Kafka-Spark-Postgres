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


# def connection_postgres():
#     try:
#         connection = psycopg2.connect(
#             database="thedb_ofdbs", user="postgres", password="bingbong300", host="localhost", port="5432")
#         print("success")
#         connection.close()
#     except psycopg2.OperationalError as e:
#         print(f"OperationalError: {e}")
#     except Exception as e:
#         print(f"Unexpected Error: {e}")


def basic_consume(consumer):
    try:
        consumer.subscribe(['emergency_incident'])

        consumer.poll(0)

        while running:
            msg = consumer.poll(timeout=10.0)
            if msg is None:
                continue
            else:
                message = msg.value().decode('utf-8')
                print(message)
                # print('Received message: {}'.format(
                #     msg.value().decode('utf-8')))
    except Exception as e:
        print(e)
    finally:
        consumer.close()


if __name__ == '__main__':
    # connection_postgres()
    # basic_consume(consumer)
