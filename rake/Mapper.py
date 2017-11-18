#!/usr/bin/env python
"""A Rake Mapper"""
"""output separate key and value by comma!"""

import sys
sys.path.append("..")
from mod.CxExtractor import CxExtractor as extractor
import mod.rake as rake
import operator
import re
import conf

def read_input(file):
    for line in file:
        yield line


def main(separator=','):
    cx = extractor()
    rake_object = rake.Rake(conf.STOPWORD, 2, 3, 1)

    # input comes from STDIN (standard input)
    url_list = read_input(sys.stdin)

    for url in url_list:
        html = cx.getHtml(url)
        if html:
            #print url
            content = cx.getText(cx.filter_tags(html))
            # write the results to STDOUT
            keywords = rake_object.run(content)
            for keyword,score in keywords[:20]:
                try:
                    print '%s%s%d' % (keyword, separator, score)
                except Exception as e:
                    pass


if __name__ == "__main__":
    main()
