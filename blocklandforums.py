from bs4 import BeautifulSoup
import requests
from xml import *

def class_window(test):
	return test.name == "p" and (test['class'] == [u'windowbg'] or test['class'] == [u'windowbg2']) 

def remove_tags(text):
	return str(BeautifulSoup(str(text)).text)

class Post:
	def __init__(self, poster, text):
		self.poster = poster
		self.text = text

class Topic:
	def __init__(self, name, poster, url):
		self.name = name.encode('utf-8')
		self.poster = poster
		self.url = url

	def get_posts(self, page=1):
		plosts = []
		page = 15 * (page - 1)
		soup = BeautifulSoup(requests.get(self.url[:-5] + str(page) + ";wap2").text)
		#body = soup.body
		if page == 0:
			posts = soup.find_all(class_window)[1:-2]
		else:
			print page
			posts = soup.find_all(class_window)[1:-3]
			#print posts
		for post in posts:
			#print "####"
			#print post
			poster = (post.text.split('\n')[1])[:-1]
			#print poster
			ocontents = post.contents[4:-3]
			contents = u''
			for content in ocontents:
				contents += unicode(content).strip()
			contents = BeautifulSoup(contents).prettify()
			plost = Post(poster, contents)
			plosts.append(plost)
		return plosts

class Board:
	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.sub_boards = {}

	def get_topics(self, page=1): #first pge (mainpage)
		topics = []

		page = 9 * (page-1)
		url = self.url[:-5] + str(page) + ";wap"
		text = requests.get(url).text
		soup = BeautifulSoup(text)
		posts = soup.find_all('p')[2:]
		for post in posts:
			cont = post.contents
			if str(cont[0]) == "- ":
				pass
			else:
				if len(cont) == 3:
					url = cont[0]
					poster = str(cont[1])[3:]
					name = url.text
					url = url['href']
					topic = Topic(name, poster, url)
					topics.append(topic)

		return topics

class Category:
	def __init__(self, name):
		self.name = name
		self.boards = {}
	def newBoard(self, name, url):
		self.boards[name] = Board(name, url)

class BlocklandForums:
	def __init__(self):
		self.categories = {}

		r = requests.get("http://forum.blockland.us/index.php?;wap")
		soup = BeautifulSoup(r.text)
		catts = soup.wml.contents[1]
		cats = catts.contents
		new = []
		for cat in cats:
			if str(cat) != "\n":
				car = remove_tags(cat)
				self.categories[car] = Category(car)

		cards = soup.find_all('card')[1:]
		#print cards
		for card in cards:
			#print card
			card = BeautifulSoup(str(card))
			cat = self.categories[card.card['title']]
			bs = card.find_all('a')
			for b in bs:
				cat.newBoard(b.text, b['href'])

if __name__ == "__main__":
	print BlocklandForums().categories["Files"].boards["Add-Ons"].get_topics()[4].get_posts(page=2)[0].text