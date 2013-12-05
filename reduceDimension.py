from utils import *

'''
	read the Feature vector file and generate SVD vectors.
	and save them.
'''

if __name__ == '__main__':

	npzfile = load(FEATURE_VEC_DIR)

	if npzfile:
		A = npzfile['arr_0']

		U, S, Vt = svd(A)
		Snew = zeros([U.shape[1], Vt.shape[0]])
		for i in range(len(S)):
			Snew[i, i] = S[i]

		dims = NUMBER_OF_DIMS
		k = min(U.shape[1], Vt.shape[0])
		if dims > k:
			print "ERROR: your dimension size is too big, largest possible dimension :", k
		else:
			Sk = Snew[0:dims, 0:dims]
			Uk = U[:, 0:dims]

			Multiplier = dot(inv(Sk), Uk.transpose())
			reducedVectors = dot(Multiplier, A)
			print "Vectors have been generated"

			savez(SVD_VEC_DIR, Multiplier, reducedVectors)
			print "Done saving Vectors"
	else:
		print "Error: Please extract features first!"


