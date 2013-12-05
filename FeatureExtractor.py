
from utils import *

'''
	Module to mine the documents and get their term counts (feature vectors)
'''

class FeatureExtractor:

	def __init__(self):

		self.wordDict = {}
		self.filenames = []
		self.dcount = 0
		self.textProcessor = TextProcessor()

	def processAllDocs(self):

		'''
			Get a dictionary of mined words and the documents associated with them
		'''
		for filename in os.listdir(DATASET_DIR):

			docString = parseXmlDoc(DATASET_DIR + filename) + parseXmlElements(DATASET_DIR + filename)
			stemmed_words = self.textProcessor.processText(docString)
			if len(stemmed_words) != 0:
				self.filenames.append(filename)

				for word in stemmed_words:
					if word in self.wordDict:
						self.wordDict[word].append(self.dcount)
					else:
						self.wordDict[word] = [self.dcount]	

				self.dcount += 1

	def build(self):

		'''
			convert the dictionary to a matrix of term counts in documents
		'''
		self.keys = [k for k in self.wordDict.keys()]
		self.keys.sort()
		self.A = zeros([len(self.keys), self.dcount])
		for i, k in enumerate(self.keys):
			for d in self.wordDict[k]:
				self.A[i,d] += 1

	def TFIDF(self):

		'''
			Perform TFIDF on the above matrix
		'''
		WordsPerDoc = sum(self.A, axis=0)
		self.DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
		self.rows, self.cols = self.A.shape
		for i in range(self.rows):
			for j in range(self.cols):
				if WordsPerDoc[j] != 0:	#some wsdl have no documentation
					self.A[i,j] = (float(self.A[i,j]) / WordsPerDoc[j]) * log(float(self.cols) / self.DocsPerWord[i])

	def saveAllVectors(self):

		'''
			save self.A, DocsPerWord to be used by SearchEngine.py
		'''
		savez(FEATURE_VEC_DIR, self.A, self.DocsPerWord)

	def saveWordList(self):

		'''
			save the list of words, we need the list in SearchEngine.py to convert query to Vector.
		'''
		saveString = "\n".join(self.keys)
		with open(WORDL_DIR, 'w') as f:
			f.write(saveString)

	def saveFilenames(self):

		'''
			save the filenames, we need the list in SearchEngine.py.
		'''
		saveString = "\n".join(self.filenames)
		with open(FILENAME_DIR, 'w') as f:
			f.write(saveString)




