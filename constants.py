'''
	Constants required for the other programs.
'''

#Required for similarity metric selection.
COSINE = 0
NORM = 1
CHEBYSHEV = 2
CORRELATION = 3

#Directory for dataset vectors etc.
DATASET_DIR = '../small_set/'					
DATA_DIR = '../data/'
HTML_DIR = '../html/display.html'
FEATURE_VEC_DIR = DATA_DIR + 'feature_vectors.npz'
SVD_VEC_DIR = DATA_DIR + 'svd_vectors.npz'
FILENAME_DIR = DATA_DIR + 'filenames.txt'
WORDL_DIR = DATA_DIR + 'wordList.txt'

#Words to be ignored.
STOP_WORDS =['a','is','an','it','at','which','that','on','the','and','where', 'then','so', 'some','them',
'their','by', 'if', 'into', 'but', 'be', 'been', 'has', 'have', 'had','hav', 'he', 'she', 'until', 'to', 'are',
'for', 'was', 'after', 'against', 'also', 'what', 'why', 'who', 'whom', 'were', 'you', 'your', 'get', 'put', 
'out', 'take', 'give', 'want']
#number of search results to be obtained
NUMBER_OF_RETURNS = 40
#number of reduced dimensions.
NUMBER_OF_DIMS = 200
