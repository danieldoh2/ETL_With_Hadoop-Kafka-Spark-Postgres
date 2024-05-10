!/bin/bash

kafka-console-consumer.sh --topic "health_events" --bootstrap-server 44.201.154.178:9092 | \
while IFS= read -r message; do
    # Check if the message contains valid JSON data
    if ! echo "$message" | jq -e . >/dev/null 2>&1; then
        echo "Skipping non-JSON message: $message"
        continue
    fi

  

    # Trim newline character at the end of the message
    message=$(echo "$message" | tr -d '\n')

    # Extract EventType and Severity from the message using jq
    event_type=$(echo "$message" | jq -r '.EventType')
    severity=$(echo "$message" | jq -r '.Severity')

    # Debug: Print the extracted EventType and Severity
    echo "Extracted EventType: $event_type"
    echo "Extracted Severity: $severity"

    # Check if EventType and Severity are empty or not present
    if [[ -z "$event_type" || -z "$severity" ]]; then
        echo "Error: EventType or Severity missing or empty"
        continue  # Skip to the next message
    fi

    # List of allowed event types
    allowed_event_types=("hospital_admission" "emergency_incident" "vaccination")

    # Check if the event_type is in the list of allowed event types
    if [[ " ${allowed_event_types[@]} " =~ " $event_type " ]]; then
        # Send the message to the determined topic based on EventType
        echo "$message" | kafka-console-producer.sh \
            --broker-list 44.201.154.178:9092 \
            --topic "$event_type"
    fi

    # Send the message to the determined topic based on Severity
    echo "$message" | kafka-console-producer.sh \
        --broker-list 44.201.154.178:9092 \
        --topic "$severity"
done
