from operator import itemgetter

from utils import *

'''
	Module to get sorted results from an input query
'''

class SearchEngine:

	def __init__(self):
		'''
			load the vectors, word list and filenames
		'''
		npzfile = load(FEATURE_VEC_DIR)
		self.A = npzfile['arr_0']
		self.DocsPerWord = npzfile['arr_1']

		npzfile = load(SVD_VEC_DIR)
		self.Multiplier = npzfile['arr_0']
		self.reducedVectors = npzfile['arr_1']

		self.rows, self.cols = self.A.shape

		with open(WORDL_DIR, 'r') as f:
			self.keys = f.read().split("\n")
		
		with open(FILENAME_DIR, 'r') as f:
			self.filenames = f.read().split("\n")

		self.textProcessor = TextProcessor()

	def stringToVector(self, query):

		'''
			Convert the query string to a vector based on dictionary of words.
		'''

		retVector = zeros([len(self.keys)])
		for word in query:
			for i, k in enumerate(self.keys):
				if word == k:
					retVector[i] += 1

		return retVector

	def processQueryString(self, queryString):

		'''
			Same as the processing happening in FeatureExtractor module.
		'''

		queryStems = self.textProcessor.processText(queryString)
		q = self.stringToVector(queryStems)
		#perform TFIDF on the query
		sumA = sum(q)
		if sumA:
			for i in range(self.rows):
				q[i] = float(q[i]) / sumA * float(log(self.cols)) / self.DocsPerWord[i]
		else:
			raise Exception("ERROR while normalizing probably your search query doesnt exist in dictionary consider enriching.")

		return q

	def getFilesByIndex(self, sortedDist):

		'''
			Get the filenames and their associated distance from query.
		'''
		for i in range(NUMBER_OF_RETURNS):
			yield (self.filenames[sortedDist[i][0]], sortedDist[i][1])

	def getNaiveSortedDist(self, q, metric):

		'''
			Get distances based on metric and sort the results.
		'''
		B = self.A.transpose()

		similarityFunction = getSimilarityFunction(metric)
		dist = [similarityFunction(b, q) for b in B]

		sortedDist = sorted(enumerate(dist), key=itemgetter(1)) 
		return sortedDist

	def getSVDSortedDist(self, q, metric):

		queryReduced = dot(self.Multiplier, q)
		similarityFunction = getSimilarityFunction(metric)

		#sim = [similarityFunction(queryReduced, b) for b in self.reducedVectors.transpose()]
		sim = dot(queryReduced, self.reducedVectors)
		
		#negating similarity
		sim = [-a for a in sim]
		
		for i in range(len(sim)):
			
			divider = float(norm(self.reducedVectors[:, i]))
			sim[i] = (sim[i] / divider)

		sortedDist = sorted(enumerate(sim), key=itemgetter(1))
		return sortedDist

	def normalSearch(self, queryString, metric):

		return self.getFilesByIndex(self.getNaiveSortedDist(self.processQueryString(queryString), metric))

	def svdSearch(self, queryString, metric):

		return self.getFilesByIndex(self.getSVDSortedDist(self.processQueryString(queryString), metric))