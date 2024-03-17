# Project Overview: Epidemic Engine Data Pipeline

As described in the syllabus (but not exactly) this project integrates several key technologies---Hadoop, Apache Spark, Apache Kafka, Apache Flink, and Apache Airflow---to build a comprehensive data pipeline for monitoring, processing, and analyzing health-related data to predict potential health risks.
The project is divided into 3 sub-projects in keeping with the grading in the syllabus. The sub-projects may have further sub-parts to ensure progress is continuously being made.
At the end, your team should have an end-to-end solution that simulates the core functionality of an \"Epidemic Engine.\"

## Project 1

### Part 1: Batch Data Analysis with Hadoop

#### Objective

Use Hadoop and MapReduce for batch processing of health event data to
uncover trends or patterns.

#### Getting Started

You have been provided a docker-compose.yml that will launch hadoop.
However, you have to run it as "root".
You have also been provided an example that will test the running instance of hadoop.
In order to run the example, you will need to use `make` as the commands are in a `Makefile`.
`make` is avaailable for every OS or, if you really want to be fancy, you can run it from a container.

What's tricky is that the example is written in java and your solution needs to be in Python.
In addition, the source code is not provided (it is probably available online just not supplied here).
We have provided you a template of how to run a python mapper & reducer.
You do need to supply the code in `word_count_python/mapper.py` & `word_count_python/mapper.py` if you want the python example to work.
I would recommend:

1. implement the word counter mapper and reducer
2. then, use the same pattern and change the mapper and reducer for each of the tasks

#### Provided

```
hadoop
├── docker-compose.yml -- launches hadoop
├── hadoop.env -- config file for hadoop that should "just work"
├── Makefile -- launches example & has a placeholder for your solution
├── simulated_health_events.csv -- data to operate on
├── word_count_java
│   ├── Dockerfile -- example container
│   ├── run.sh -- example runner
│   └── WordCount.jar -- java code for mapreduce
└── word_count_python
    ├── Dockerfile -- example container
    ├── mapper.py -- python mapper placeholder
    ├── reducer.py -- python reducer placeholder
    ├── run.sh -- example runner
    └── sources.list -- solution for getting python installed in the container
```

#### Tasks

* Write a MapReduce job to count the number of events by type.
* Aggregate events by location to identify high-risk areas.

#### Requirements

* When we git clone your repo, your solution should run using `make hadoop_solved`.
* Your `make target` should *not* launch hadoop

#### Tips

Here are some things that may be helpful while you are trying to build this solution.

* Your biggest challenge will likely be keeping track of the context all of your commands are running in.
  This can be super confusing so keep it in mind while debugging.
* If you get `PipeMapRed.waitOutputThreads(): subprocess failed with code 127` or something similar when trying to run your job, one of these is likely:
  * Your code isn't running properly, make sure it will run locally and locally in the container.
  You can get the log file by doing something like `yarn logs -applicationId application_1426769192808_0004` in the `namenode` see [stack overflow](https://stackoverflow.com/questions/29164388/hadoop-streaming-job-failing) for some hints.
  * You may need to restart your hadoop server w/ `<cmd> compose down && <cmd> compose up -d` because it is in a bad state.
* Handy hadoop commands (fyi `hdfs dfs` has been replaced by `hadoop fs`)
  * `hadoop fs -ls -R / | less # print the file listing recursively`
  * `hadoop fs -rm -r /output # remove the output dir`
  * `hadoop fs -get /local-output-reduced ./ # get a file from the hdfs filesystem`
  * `hadoop fs -put ./simulated_health_events.csv /input/ # put a file in hdfs to make it available to hadoop`



### Part 2: Real-time Stream Processing with Apache Flink

#### Objective

Implement real-time data processing using Apache Flink to identify immediate trends or anomalies in health event data.

#### Tasks

TBD

## Project 2
### Part 1: Data Ingestion and Categorization with Kafka

#### Objective

Develop a Kafka-based system to ingest and categorize incoming health event data.

#### Tasks

TBD

### Part 2: Advanced Analytics with Apache Spark

#### Objective

Leverage Apache Spark for in-depth analysis of health event data to predict potential health risks.

#### Tasks

TBD

### Part 3: Workflow Orchestration with Apache Airflow

#### Objective

Orchestrate the entire data pipeline using Apache Airflow, ensuring each component is executed efficiently and in the correct order.

#### Tasks

TBD

## Project 3
### Part 1: Data Visualization and Reporting

#### Objective

Create visual representations of the processed data to highlight key findings and trends.

#### Tasks

TBD

### Part 2: Final Integration, Connecting the Parts

Objective: Integrate all the components developed to establish an end-to-end data pipeline that simulates the Epidemic Engine, demonstrating the flow from data ingestion to visualization.

#### Tasks

TBD

