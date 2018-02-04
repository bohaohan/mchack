import urllib.request
from bs4 import BeautifulSoup
import feedparser

news_url = 'https://www.cnn.com/2018/02/03/politics/paul-ryan-tweet-tax-cut-backlash/index.html'
news_url2 = 'https://www.cnn.com/2018/02/03/politics/democratic-california-house-candidates-nunes-memo/index.html'
def cnnarticlescraper(url):
	'''This function takes a URL to a CNN news article and scrapes the article headline, text, and url using Beautiful Soup'''
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	headline = soup.find('h1',{'class':'pg-headline'}) #Scrapes headline in article.
	raw = soup.find_all(['div','p'],{"class":'zn-body__paragraph'}) #Scrapes text
	text = ''
	for item in raw:
		text += " " + item.text
	print(headline.text)
	print(text)
	print(url)

def cnnrssscraper(headlinenumber):
	'''Uses the CNN RSS to take in the current headlines of the CNN frontpage'''
	frontpage = feedparser.parse('http://rss.cnn.com/rss/cnn_topstories.rss')
	numberofheadlines = 0
	for entrynum in range(len(frontpage.entries)):
		if frontpage.entries[entrynum]['link'].endswith('.html') and numberofheadlines < headlinenumber: #Checks how many headlines have been displayed and if the link is an actual news article
			print(frontpage.entries[entrynum]['title'])
			print(frontpage.entries[entrynum]['published']) #Returns article publication time.
			print(frontpage.entries[entrynum]['link'])
			print(cnnarticlescraper(frontpage.entries[entrynum]['link']))
			numberofheadlines += 1
		else:
			continue

def cbcarticlescraper(url):
	'''This function takes a URL to a CBC news article and scrapes the article headline, text, and url using Beautiful Soup'''
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	headline = soup.find('h1',{'class':'story-title'}) #Scrapes headline in article
	raw = soup.find_all('div', {'class':'story-content'}) #Scrapes text
	text = ''
	for item in raw:
		text += " " + item.text
	print(headline.text)
	print(text)
	print(url)


def cbcrssscraper(headlinenumber):
	'''Uses the CBC RSS to take in the current headlines of the CNN frontpage'''
	frontpage = feedparser.parse('http://www.cbc.ca/cmlink/rss-topstories')
	numberofheadlines = 0
	for entrynum in range(len(frontpage.entries)):
		if numberofheadlines < headlinenumber:
			print("=" * 20)
			#Returns article title, publication time, and link, and then runs the article scraper to get the text.
			print(frontpage.entries[entrynum]['title'])
			print(frontpage.entries[entrynum]['published'])
			print(frontpage.entries[entrynum]['link'])
			print(cbcarticlescraper(frontpage.entries[entrynum]['link']))
			print("\n" + "="*20)
			numberofheadlines += 1
		else:
			continue

def abcarticlescraper(url):
	'''This function takes a URL to a ABC news article and scrapes the article headline, text, and url using Beautiful Soup'''
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	headline = soup.find('header', {'class':"article-header"}).h1
	raw = soup.find_all('p', {'itemprop':'articleBody'})
	text = ''
	for item in raw:
		text += " " + item.text
	print(headline.text)
	print(text)
	print(url)

def abcrssscraper(headlinenumber):
	'''Uses the ABC RSS to take in the current headlines of the CNN frontpage'''
	frontpage = feedparser.parse('http://abcnews.go.com/abcnews/topstories')
	numberofheadlines = 0
	for entrynum in range(len(frontpage.entries)):
		if numberofheadlines < headlinenumber:
			print("=" * 20)
			print(frontpage.entries[entrynum]['title'])
			print(frontpage.entries[entrynum]['published'])
			print(frontpage.entries[entrynum]['link'])
			print(abcarticlescraper(frontpage.entries[entrynum]['link']))
			print("\n" + "="*20)
			numberofheadlines += 1
		else:
			continue

#Test cases.
# abcrssscraper(5)
# cbcrssscraper(5)
# # cnnarticlescraper(news_url)