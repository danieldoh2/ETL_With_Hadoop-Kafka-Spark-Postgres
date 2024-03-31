FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

# fixes lack of python in the container
# and that the version of the OS is deprecated
ADD sources.list /etc/apt/sources.list
RUN apt update || : # ignore error
RUN apt install -y python3 python3-pip

# create a directory for the app
RUN mkdir /app
WORKDIR /app
# add the mapper, reducer
ADD location_mapper.py ./
ADD location_reducer.py ./
RUN chmod a+x ./*

ENV MAPPER="location_mapper.py"
ENV REDUCER="location_reducer.py"
ENV INPUT="/input/simulated_health_events.csv"
ENV DATA_LOC="/app/simulated_health_events.csv"
ENV DEBUG='false'


ADD run.sh /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]
