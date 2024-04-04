from confluent_kafka import Consumer, KafkaError

# Configure Kafka consumer
conf = {
    'bootstrap.servers': '44.201.154.178:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'  # Start consuming from the beginning of the topic
}

# Create Kafka consumer
consumer = Consumer(conf)

# Subscribe to topic


running = True


def basic_consume(consumer, topics):
    try:
        consumer.subscribe(['health_events'])
        while running:
            msg = consumer.poll(timeout=10.0)
            if msg is None:
                continue
            else:
                print('Received message: {}'.format(
                    msg.value().decode('utf-8')))

    except Error:
        pass
    finally:
        consumer.close()
