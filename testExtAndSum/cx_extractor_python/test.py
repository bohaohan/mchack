from hackthon.mchack.testExtAndSum import CxExtractor

cx = CxExtractor(threshold=186)
html = cx.getHtml("https://www.theguardian.com/football/2018/feb/03/manchester-united-huddersfield-town-premier-league-match-report")
# html = cx.getHtml("http://news.163.com/17/0810/09/CRFF02Q100018AOR.html")
content = cx.filter_tags(html)
s = cx.getText(content)
print(s)
