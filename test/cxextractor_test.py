import sys
sys.path.append("..")

from mod.CxExtractor import CxExtractor as extractor
cx = extractor()
# test_html = cx.readHtml("E:\\Documents\\123.html")
url = 'https://docs.google.com/presentation/d/1UeKXVgRvvxg9OUdh_UiC5G71UMscNPlvArsWER41PsU/edit#slide=id.gc2fcdcce7_216_128'
test_html = cx.getHtml(url)
content = cx.filter_tags(test_html)
print content
s = cx.getText(content)
print s
