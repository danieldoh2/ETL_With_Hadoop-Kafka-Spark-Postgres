
# from confluent_kafka import Consumer, KafkaError
# import pandas as pd


# def basic_consume(consumer):
#     running = True
#     try:
#         consumer.subscribe(['low'])

#         # Seek to the end of the partitions before starting to consume messages
#         # This is necessary to ensure we actually join the group
#         consumer.poll(0)

#         while running:
#             msg = consumer.poll(timeout=10.0)
#             if msg is None:
#                 continue
#             else:

#                 print('Received message: {}'.format(
#                     msg.value().decode('utf-8')))
#                 msg = msg.value().decode('utf-8')
#                 msg = msg.pop()
#                 print("this is new msg: ", msg)
#                 print(type(msg))

#     except Exception as e:
#         print("Error: ", e)
#     finally:
#         consumer.close()


# def main():

#     # Configure Kafka consumer
#     conf = {
#         'bootstrap.servers': '44.201.154.178:9092',
#         'group.id': 'my_consumer_group',
#         'auto.offset.reset': 'latest'  # Start consuming from the latest offset of the topic
#     }

#     # Create Kafka consumer
#     consumer = Consumer(conf)
#     basic_consume(consumer)


if __name__ == '__main__':
    str = '{"EventType": "routine_checkup", "Timestamp": "2024-04-15 02:23:54", "Location": "Los Angeles", "Severity": "low", "Details": "This is a simulated routine_checkup event."}'
    n_str = str(2:)
    print(n_str)
    # main()
