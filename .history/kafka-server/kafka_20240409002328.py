from confluent_kafka import Consumer, KafkaError

# Configure Kafka consumer
conf = {
    'bootstrap.servers': '44.201.154.178:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'latest'  # Start consuming from the latest of the topic
}

# Create Kafka consumer
consumer = Consumer(conf)

running = True


def basic_consume(consumer):
    try:
        consumer.subscribe(['test_topic'])
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
    basic_consume(consumer)
