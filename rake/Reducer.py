#!/usr/bin/env python
"""A Rake Reducer"""

import sys
sys.path.append("..")

from itertools import groupby
from operator import itemgetter
import mod.rake as rake
import conf

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator=','):
    # input comes from STDIN (standard input)
    data = read_mapper_output(sys.stdin, separator=separator)
    rake_object = rake.Rake(conf.STOPWORD, 2, 3, 1)

    '''
    for current_word, group in groupby(data, itemgetter(0)):
        total_score = sum(int(score) for current_word, score in group)
        print "%s%s%d" % (current_word, separator, total_score)

    '''

    wordlist = []
    for current_word, group in groupby(data, itemgetter(0)):
        total_score = sum(int(score) for current_word, score in group)
        if total_score > 2:
            #print "%s%s%d" % (current_word, separator, total_score)
            wordlist.append([current_word,total_score])

    wordlist_sort = sorted(wordlist, key=lambda a:a[1], reverse=True)
    for word, score in wordlist_sort[:1000]:
        print "%s%s%d" % (word, separator, score)



    '''
    wordlist = {}
    for current_word, group in groupby(data, itemgetter(0)):
        try:
            total_score = sum(int(score) for current_word, score in group)
            if total_score > 10:
                if current_word.lower() in wordlist:
                    wordlist[current_word.lower()] += total_score
                else:
                    wordlist[current_word.lower()] = total_score

        except ValueError:
            # count was not a number, so silently discard this item
            pass


    wordlist_sort = sorted(wordlist, key=wordlist.get, reverse=True)

    for current_word in wordlist_sort:
        total_score = wordlist[current_word]
        print "%s%s%d" % (current_word, separator, total_score)
    '''


if __name__ == "__main__":
    main()
