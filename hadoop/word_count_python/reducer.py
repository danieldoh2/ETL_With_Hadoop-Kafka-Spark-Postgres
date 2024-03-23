#!/usr/bin/env python3
"""reducer.py"""

# input comes from STDIN (standard input)
# write some useful code here and print to STDOUT

import sys

def reduce():
    counts = {}
    for line in sys.stdin:
        word, count = line.strip().split('\t')

        if word in counts:
            counts[word] += int(count)
        
        else:
            counts[word] = int(count)

    
    del counts['EventType ']
    del counts['Location ']
    
    for word, count in counts.items():
        print(word, count)


    
def main():
    reduce()


if __name__ == '__main__':
    main()

