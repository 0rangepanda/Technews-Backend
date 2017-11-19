#!/usr/bin/env python
"""A more advanced Mapper, using Python iterators and generators."""

import sys
sys.path.append("..")
from mod.CxExtractor import CxExtractor as extractor
import re

def read_input(file):
    for line in file:
        yield line

def wordcount(content, separator, regexPattern):
    #for word in content.split():
    for word in re.split(regexPattern, content):
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        print '%s%s%d' % (word, separator, 1)


def main(separator='\t'):
    cx = extractor()
    # input comes from STDIN (standard input)
    url_list = read_input(sys.stdin)
    delimiters = " ", "\n", "\t", ".", ",", "(", ")", "\"", "\'"
    regexPattern = '|'.join(map(re.escape, delimiters))

    for url in url_list:
        html = cx.getHtml(url)
        if html:
            #print url
            content = cx.getText(cx.filter_tags(html))
            # write the results to STDOUT
            wordcount(content.encode("utf8"), separator, regexPattern)


if __name__ == "__main__":
    main()
