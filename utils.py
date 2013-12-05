import os
from xml.etree import ElementTree
from stemming.porter2 import stem
import string
from nltk.corpus import wordnet as wn
import re
from constants import *	
from scipy.linalg import *
from scipy.spatial import distance
from numpy import *
import string 
import enchant

def enrich(queryString):

	'''
		enrich the query string by adding synonyms to it
	'''

	words = queryString.split(" ")
	mySet = set()
	for word in words:

		mySet.add(word)
		synonyms = wn.synsets(word)

		for syn in synonyms:

			mySet.add(syn.name.split('.')[0])

	return " ".join(mySet)

def destroyer(filename):

	'''
		This function is used in deleter.py given a filename delete it if it does not have a documentation
	'''
	with open(filename, 'rt') as f:
		tree = ElementTree.parse(f)

	toDelete = 1
	for node in tree.iter():
		if '}' in node.tag:
			tag = node.tag.split('}')[1]			#ignore the namespace if it is there
		else:
			tag = node.tag

		if tag == 'documentation' and node.text:
			toDelete = 0
			break

	if toDelete:
		os.system('rm '+ filename)

	return toDelete
			

def parseXmlDoc(filename):

	'''
		Get the documentation text of the xml document
	'''

	with open(filename, 'rt') as f:
		tree = ElementTree.parse(f)

	docList = []
	for node in tree.iter():
		if '}' in node.tag:
			tag = node.tag.split('}')[1]			#ignore the namespace if it is there
		else:
			tag = node.tag

		if tag == 'documentation' and node.text:			
			docList.append(node.text)
			#break

	docString = ' '.join(docList)
	return docString.encode('ascii', 'ignore') #convert to ascii

def parseXmlElements(filename):

	'''
		Get the element tag name data (useful for files that dont have documentation)
	'''

	with open(filename, 'rt') as f:
		tree = ElementTree.parse(f)

	docList = set()
	for node in tree.iter():
		if '}' in node.tag:
			tag = node.tag.split('}')[1]			#ignore the namespace if it is there
		else:
			tag = node.tag

		if tag == 'element' and node.get("name"):			
			docList.add(node.get("name"))
			#break

	docString = ' '.join(docList)
	return camelCaseSplitter(docString.encode('ascii', 'ignore')) #convert to ascii

class TextProcessor:

	def __init__(self):

		self.d = enchant.Dict("en_US")
		
	def processText(self, docText):

		#convert to lowercase.
		text = docText.encode('ascii', 'ignore').strip().replace("\n"," ").lower()
		#remove html tags
		text = re.sub('<[^>]*>', '', text)
		#remove &; from html
		text = re.sub('&[^;]*;', '', text)
		#remove multiple spaces
		text = re.sub(' +',' ', text)
		#remove puncutuations
		text = text.translate(string.maketrans("",""), string.punctuation)
		#remove stop words and stem it.
		words = [word for word in text.split(' ')\
		 if word not in STOP_WORDS and all([c.isalpha() for c in word]) and len(word) > 2 and len(word) < 20]
		words = [word for word in words if self.d.check(word)]	 
		return [stem(word) for word in words]

def camelCaseSplitter(docString):

	'''
		Split camelCase letters ( this is useful for splitting element tag name data)
	'''

	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', docString)
	s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower().split('_')
	s1 = [word.strip() for word in s1 if len(word) > 2]
	return ' '.join(s1)

'''
	Below are various distance metrics
'''

def getSimilarityFunction(metric):
	
	if metric == COSINE:
		return distance.cosine
	elif metric == CHEBYSHEV:
		return distance.chebyshev
	elif metric == CORRELATION:
		return distance.correlation
	else:
		return normalizedEuclidean

def normalizedEuclidean(vec1, vec2):

	return norm(vec1 - vec2)


