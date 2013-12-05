'''
	Script used for deleting files that dont have a documentation.
	This was needed before but now we have a metadata module which
	can get element tag data.
'''

from utils import *

if __name__ == '__main__':

	count = 0;
	for filename in os.listdir(DATASET_DIR):
		count += destroyer(DATASET_DIR + filename)

	print count