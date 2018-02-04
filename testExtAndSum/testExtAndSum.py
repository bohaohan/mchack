__author__ = 'bohaohan'
from CxExtractor import *
from main_ import *
from keywordextractor import *


def testExtAndSum(url):
    cx = CxExtractor(threshold=186)
    html = cx.getHtml(url)
    # print html
    pattern = "<title.*?>(.+?)</title>"
    titles = re.findall(pattern, html)
    print "titles", titles
    content = cx.filter_tags(html)
    s = cx.getText(content)
    sum_ = summarize(s, 3)
    kws = keyword_analysis(sum_)
    return sum_, titles[0], kws


if __name__ == '__main__':
    url = "https://www.theguardian.com/football/2018/feb/03/manchester-united-huddersfield-town-premier-league-match-report"
    # testExtAndSum(url)
    sum_, title, kws = testExtAndSum(url)
    print kws
