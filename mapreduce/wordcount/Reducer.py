#!/usr/bin/env python
"""A more advanced Reducer, using Python iterators and generators."""

from itertools import groupby
from operator import itemgetter
import sys

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_mapper_output(sys.stdin, separator=separator)
    # groupby groups multiple word-count pairs by word,
    # and creates an iterator that returns consecutive keys and their group:
    #   current_word - string containing a word (the key)
    #   group - iterator yielding all ["&lt;current_word&gt;", "&lt;count&gt;"] items
    stoplist = []
    with open('stopword', 'r') as f:
        for line in f:
            stoplist.append(line[:-1])

    wordlist = {}
    for current_word, group in groupby(data, itemgetter(0)):
        try:
            total_count = sum(int(count) for current_word, count in group)
            #print "%s%s%d" % (current_word, separator, total_count)
            if total_count > 10:
                if current_word.lower() in wordlist:
                    wordlist[current_word.lower()] += total_count
                else:
                    wordlist[current_word.lower()] = total_count

        except ValueError:
            # count was not a number, so silently discard this item
            pass


    wordlist_sort = sorted(wordlist, key=wordlist.get, reverse=True)

    for current_word in wordlist_sort:
        total_count = wordlist[current_word]
        if not (current_word in stoplist):
            print "%s%s%d" % (current_word, separator, total_count)


if __name__ == "__main__":
    main()
