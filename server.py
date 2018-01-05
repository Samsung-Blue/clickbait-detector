from bs4 import BeautifulSoup
import re
import nltk
import collections
import operator
import random
import requests
from bs4.element import Comment
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import sentiwordnet as swn
from flask import Flask, request

app = Flask(__name__)
app.debug = True

############### Global Variables ##################

stopwords = set(stopwords.words('english'))

baitlines = []
nonbaitlines = []
clickbaits = 0

# Global variables
labels = []
bait = []
nonbait = []
bait_dictionary = {}
nonbait_dictionary = {}

def getFrequencies():

	global labels, bait_dictionary, nonbait_dictionary, baitlines, nonbaitlines

	with open('clickbait.txt') as f:
		for line in f:
			baitlines.append(line.decode('utf-8'))

	with open('genuine.txt') as f:
		for line in f:
			nonbaitlines.append(line.decode('utf-8'))

	for line in baitlines:
		word_tokens = word_tokenize(line)
		for word in word_tokens:
			word = word.lower()
			match = re.search("[.,\/#!$%\^&\*;:\{\}=\-_`~()'?0123456789+]", word)
			if (match == None and word not in stopwords):
				bait.append(word)

	for line in nonbaitlines:
		word_tokens = word_tokenize(line)
		for word in word_tokens:
			word = word.lower()
			match = re.search("[.,\/#!$%\^&\*;:\{\}=\-_`~()'?0123456789+]", word)
			if (match == None and word not in stopwords):
				nonbait.append(word)


	bait_dictionary = collections.Counter(bait)
	nonbait_dictionary = collections.Counter(nonbait)

def checkClickBaitness(sentence):
	global clickbaits
	word_tokens = word_tokenize(sentence)
	p_bait = 1
	p_nonbait = 1
	for word in word_tokens:
		word = word.lower()
		match = re.search("[.,\/#!$%\^&\*;:\{\}=\-_`~()'?0123456789+]", word)
		if (match == None and word not in stopwords):
			if word in bait_dictionary:
				if word in nonbait_dictionary:
					p_bait = p_bait * bait_dictionary[word]
					p_nonbait = p_nonbait * nonbait_dictionary[word]
				else:
					p_nonbait = p_nonbait * 0.5
			else:
				if word in nonbait_dictionary:
					p_bait = p_bait * 0.5

	if p_bait > p_nonbait:
		clickbaits = clickbaits + 1
		print sentence

def tag_visible(element):
	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True

def getClickbaitPercentage(url):
	global clickbaits

	getFrequencies()
	post = requests.get(url)
	soup = BeautifulSoup(post.content, 'html.parser')
	tags = soup.find_all(text=True)
	visible_texts = filter(tag_visible, tags)
	total = 0
	clickbaits = 0
	sentences = (t.strip() for t in visible_texts)
	for sentence in sentences:
		if(sentence != ''):
			total = total + 1
			checkClickBaitness(sentence)

	if(total != 0):
		return clickbaits * 100.0 / total
	else:
		return 0

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
		url = request.form["url"]
		clickbait = str(getClickbaitPercentage(url))
		return clickbait 

if __name__ == "__main__":
    app.run()