#!/usr/bin/python
import sys
import re
import operator
from itertools import groupby
from operator import itemgetter


def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator=','):
    # input comes from STDIN (standard input)
    data = read_mapper_output(sys.stdin, separator=separator)

    wordlist = []
    for current_word, group in groupby(data, itemgetter(0)):
        total_score = sum(int(score) for current_word, score in group)
        if total_score > 2:
            #print "%s%s%d" % (current_word, separator, total_score)
            wordlist.append([current_word,total_score])

    wordlist_sort = sorted(wordlist, key=lambda a:a[1], reverse=True)
    for word, score in wordlist_sort[:2000]:
        print ("%s%s%d" % (word, separator, score, ))


if __name__ == "__main__":
    main()
