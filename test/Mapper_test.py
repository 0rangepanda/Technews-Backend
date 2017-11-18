#!/usr/bin/env python
"""A more advanced Mapper, using Python iterators and generators."""

import sys
sys.path.append("..")

from mod.CxExtractor import CxExtractor as extractor
import mod.rake as rake
import operator

def read_input(file):
    for line in file:
        yield line



def main(separator=','):
    cx = extractor()
    rake_object = rake.Rake("./stopword", 2, 3, 2)

    # input comes from STDIN (standard input)
    urlfile = open('./url_list', 'r')
    url_list = read_input(urlfile)
    for url in url_list:
        html = cx.getHtml(url)
        if html:
            content = cx.getText(cx.filter_tags(html)).encode("utf8")
            #print content
            # write the results to STDOUT
            keywords = rake_object.run(content)
            for keyword,score in keywords[:15]:
                print '%s%s%d' % (keyword, separator, score)



if __name__ == "__main__":
    main()
