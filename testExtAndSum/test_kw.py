__author__ = 'bohaohan'
import requests
url = "http://0.0.0.0:23334/test_kw"
# url = "https://datacleanandsum.appspot.com/test_kw"
data = {
  # "url": "https://www.theguardian.com/football/2018/feb/03/manchester-united-huddersfield-town-premier-league-match-report"
    # "url": "https://datacleanandsum.appspot.com/"
    "summary": "The way he made space for a right-foot shot from the edge of the penalty area that forced a scrambling save from Jonas L\u00f6ssl was sublime, as were a couple of his passes to Mata and Antonio Valencia, yet he ended the first half furious that the referee had not awarded him a free-kick in the middle of the pitch and lost his cool to the extent that he was booked in stoppage time for an unnecessary foul on Florent Hadergjonaj. The Chilean deserved it, if only for the number of times he was fouled. \"Alexis is a fantastic player but he\u2019s not a prima donna, he\u2019s a humble guy. He came in for some attention but he\u2019s used to that, he never stopped running. He was nearly dead at the end but I think he enjoyed the game.\"Topics."
  }
r = requests.post(url, data=data)
print r.text