#/usr/local/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import entropy
from sklearn.preprocessing import binarize

def get_llrs(X, y, features, label=1, binary=True, debug_word_set=None):
    '''
    Computes Log-Likelihood Ratio (LLR) for the input features.
    Parameters:
        -----------
        X: Numpy matrix (m x n)
            Consisting of training instances as rows and features as columns
        y: numpy matrix
            The labels of the instances
        label: int (Default 1)
            consider this label as positive label and compute LLR. This value should be one of the values in y
        binary: boolean (Default True)
            If true then features are counted as binary. ie either the feature occurs in that document or not. Term freq within the document is ignored.
        debug_word_set: set()
            Prints the debug information if the feature is in this set
    Returns:
        -----------
        list of tuples of the form [(a,b), ...] where a: the feature, b: the llr score of the feature
    Usage:
        -----------
        X = count_vect.transform(data.get_texts())
        print('feat_X.shape %d,%d' % X.shape)
        y = data.target
        features = np.array(count_vect.get_feature_names())
        llrs = get_llrs(X, y, features, label=1, binary=True)
        features = np.array([item[0] for item in llrs])
        weights = np.array([item[1] for item in llrs])
    '''
    if binary:
        nc = (y == label).sum()
        nc_ = (y != label).sum()
        X = binarize(X)
    else:
        nc = X[y == label].sum()
        nc_ = X[y != label].sum()
    print('nc, nc_ = %d,%d' % (nc, nc_))
    counts = X[y == label, :]
    counts_ = X[y != label, :]
    k1h = counts.sum(axis=0) + 1
    k2h = counts_.sum(axis=0) + 1
    k1t = nc - k1h + 1
    k2t = nc_ - k2h + 1
    llrs = []
    for i,word in enumerate(features):
        if debug_word_set is not None and word not in words:
            continue
        mat = np.matrix([[k1h[0,i], k1t[0,i]], [k2h[0,i], k2t[0,i]]])
        if mat[0,0] == 1:
            continue
        # llr = 2 * mat.sum() * (-entropy(mat.A1) - -entropy(mat.sum(axis=1)) - -entropy(mat.T.sum(axis=1)))
        Hmat = entropy(mat.A1) # entropy of matrix
        Hrow = entropy(mat.sum(axis=1))[0] # entropy of row sums
        Hcol = entropy(mat.T.sum(axis=1))[0] # entropy of col sums
        llr = - 2 * mat.sum() * (Hmat - Hrow - Hcol)
        llrs.append((word, llr))
        if debug_word_set is not None and word in debug_word_set:
            print(word)
            print(mat)
            print (mat.sum(), Hmat, Hrow, Hcol)
            print(llr)
        
    return llrs

