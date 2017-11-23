#!/usr/bin/env python
import sys
sys.path.append("..")
from mod.CxExtractor import CxExtractor as extractor
import operator

def read_input(file):
    for line in file:
        yield line


def main(separator=','):
    cx = extractor()
    datasize = 0 # in Byte

    urlfile = open('./url_list_300', 'r')
    url_list = read_input(urlfile)
    for url in url_list:
        html = cx.getHtml(url)
        if html:
            content = cx.getText(cx.filter_tags(html)).encode("utf8")
            datasize += len(content)
            print datasize

    print "total datasize: ", datasize, "Byte"

if __name__ == "__main__":
    main()
