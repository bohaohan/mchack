# __author__ = 'bohaohan'
import requests
url = "http://0.0.0.0:23334/get_sum"
# url = "https://datacleanandsum.appspot.com/get_sum"
data = {
  "url": "https://www.theguardian.com/football/2018/feb/03/manchester-united-huddersfield-town-premier-league-match-report"
  }
r = requests.post(url, data=data)
print r.text
#
# # r = requests.post("http://0.0.0.0:23334/")
# # print r.text
#
# url = "https://www.theguardian.com/football/2018/feb/03/manchester-united-huddersfield-town-premier-league-match-report"
# from testExtAndSum import *
#
# sum_, title = testExtAndSum(url)
#
# print sum_, title

import urllib2
