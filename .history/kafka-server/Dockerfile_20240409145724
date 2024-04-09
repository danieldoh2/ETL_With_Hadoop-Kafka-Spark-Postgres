FROM docker.io/bitnami/kafka:3.7

# Install jq (JSON processor)
# RUN apt-get update && apt-get install -y jq

USER root
# Ensure apt lists directory exists and set proper permissions
RUN mkdir -p /var/lib/apt/lists && chmod 755 /var/lib/apt/lists
RUN mkdir -p /var/lib/apt/lists/partial


RUN apt-get update && apt-get install -y jq        


# Copy the script into the container
COPY kafka_processor.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/kafka_processor.sh

# Set the default command to run when the container starts
CMD ["kafka_processor.sh"]