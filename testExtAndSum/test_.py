__author__ = 'bohaohan'
import requests
url = "http://0.0.0.0:2333/get_sum"
data = {
  "url": "https://www.theguardian.com/football/2018/feb/03/manchester-united-huddersfield-town-premier-league-match-report"
  }
r = requests.post(url, data=data)
print r.text