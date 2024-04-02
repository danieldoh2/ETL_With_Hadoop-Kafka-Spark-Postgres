#!/usr/bin/env python3
"""mapper.py"""

# input comes from STDIN (standard input)
# write some useful code here and print to STDOUT
import sys

def map_reduce_with_stdin():

    for line in sys.stdin:
        words = line.strip().split(',')
        print(words[3], '\t', 1)


if __name__ == '__main__':
    map_reduce_with_stdin()

    
