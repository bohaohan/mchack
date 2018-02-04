__author__ = 'bohaohan'
from CxExtractor import *
from main_ import *


def testExtAndSum(url, cx=CxExtractor(threshold=186)):
    html = cx.getHtml(url)
    # print html
    # html = cx.getHtml("http://news.163.com/17/0810/09/CRFF02Q100018AOR.html")
    pattern = "<title.*?>(.+?)</title>"
    titles = re.findall(pattern, html)
    print "titles", titles
    content = cx.filter_tags(html)
    s = cx.getText(content)
    sum_ = summarize(s, 3)
    return sum_, titles[0]


if __name__ == '__main__':
    url = "https://www.theguardian.com/football/2018/feb/03/manchester-united-huddersfield-town-premier-league-match-report"
    testExtAndSum(url, cx=CxExtractor(threshold=186))