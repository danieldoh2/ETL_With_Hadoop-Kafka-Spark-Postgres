#!/usr/bin/env python3
"""mapper.py"""

# input comes from STDIN (standard input)
# write some useful code here and print to STDOUT


def map_reduce_with_stdin():
    import sys
    for line in sys.stdin:
        words = line.split(',')
        print(words[1], '\t', 1)


def map_reduce_with_opened_file():
    import sys
    sys.stdin = open('/hadoop/simulated_health_events.csv', 'r')
    for line in sys.stdin:
        words = line.split(',')
        print(words[1], '\t', 1)

# Execution of the file. if the file is run directly, it will try to run with stdin first
# If that fails, it will set stdin to the file and run the map reduce function that way


try:
    map_reduce_with_stdin()
except Exception as error:
    map_reduce_with_opened_file()
