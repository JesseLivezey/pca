import numpy as np
import scipy as sp
from scipy import linalg

#function to do pca on an array of vectors then reduce dimensionality. Always converts data into columns of data
def pca(vectors,dim,rowColumn=None):
    if rowColumn is None:
        vectors2 = vectors
    elif rowColumn == 'r':
        vectors2 = vectors.T

    centerVecs = np.zeros(vectors2.shape)
#Mean of each row
    meanVec = vectors2.mean(axis=1)
#Subtract mean
    for i in xrange(vectors2.shape[0]):
        for j in xrange(vectors2.shape[1]):
            centerVecs[i,j] = vectors2[i,j]-meanVec[i]
#Compute covariance matrix
    covMat = np.dot(centerVecs,centerVecs.T)
#Compute eigen info
    eigen = linalg.eigh(covMat)
    eValues = eigen[0]
    eVectors = eigen[1]
    idx = eValues.argsort()
    eValues = eValues[idx]
    eVectors = eVectors[:,idx]
#Project back onto a reduced dimensionality basis
    reducedDim = np.array([np.dot(np.array([eVectors[:,-1-ii]]),centerVecs)[0] for ii in xrange(dim)])

#Tranpose back to original
    if rowColumn == 'r':
        reducedDim = reducedDim.T
    return (reducedDim,eValues,eVectors,meanVec)

def reconst(reducedDim,eVectors,meanVec,rowColumn):
    if rowColumn == 'r':
        reducedDim2 = reducedDim.T
    else:
        reducedDim2 = reducedDim
    fullDim = np.zeros((eVectors.shape[1],reducedDim2.shape[1]))
    print fullDim.shape
    for ii in xrange(reducedDim2.shape[1]):
        for jj in xrange(reducedDim2.shape[0]):
            fullDim[:,ii] += eVectors[:,-1-jj]*reducedDim2[jj,ii]
    for ii in xrange(reducedDim2.shape[1]):
        fullDim[:,ii] += meanVec
    if rowColumn == 'r':
        fullDim = fullDim.T
    return fullDim

