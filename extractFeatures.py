from FeatureExtractor import *

'''
	run this script to perform feature extraction and store the vectors as files
'''

if __name__ == '__main__':

	ex = FeatureExtractor()

	ex.processAllDocs()
	print "Done processing documents"

	ex.build()
	ex.TFIDF()
	print "Done generating feature vectors"

	ex.saveAllVectors()
	ex.saveWordList()
	ex.saveFilenames()
	print "Features, wordList and filenames have been saved."