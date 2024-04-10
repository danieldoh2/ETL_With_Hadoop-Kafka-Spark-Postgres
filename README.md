## Instructions for Running Project ##

1. run `docker-compose up --build` to start docker containers

2. cd to root directory hadoop to run commands
- you can run `make-target` commands (`make event-counter` and `make location-mapreducer` to aggregate jobs by location and events 
- hadoop should not be launched locally but through docker compose file and makefile commands

3. run `make hadoop_solved` should produce solution



## Instructions for Running Project (Kafka) ##
1. cd to kafka directory.
2. Run docker-compose up. 

#Structure of Project
We have the kafka process running within 1-2 containers.
All logic for the producers/consumers are written within the kafka_processor sh script.

Our service (kafka-producer) is the container that executes the creation of consumers and producers using the kafka_processor sh script.
  1. It intercepts the stream of health_events at 44.201.154.178:9092 on the topic health_events.
  2. It utilizes jq (JSON data parser) to extract event_type and severity from the events.
  3. Using the extracted information, it dynamically creates producers that broadcast those events into the 6 appropriate topics.
     
