#/usr/local/bin/python3
# -*- coding: utf-8 -*-

import numpy as np


class SamplingClassifier:
    '''
    Creates an SVM classifier to subsample a low prevalence labeled dataset. 
    Use Sub-sampling to balance out the prevalence of the labeled data 
    and create several classifiers.
    '''
    def __init__(self, classifier, classifier_args, n_classifiers=10, sample_percent=0.1):
        self.n_classifiers = n_classifiers
        self.classifiers = [classifier(**classifier_args) 
                                for i in range(0,self.n_classifiers)]
        self.sample_percent = sample_percent


    def fit(self, X, y):
        print('input training data shape = (%d,%d)' % X.shape)
        for i in range(0,self.n_classifiers):
            sample_size = int(y.shape[0] * self.sample_percent)
            random_indices = np.random.choice(y.shape[0], sample_size)
            X_i = X[random_indices]
            y_i = y[random_indices]
            print ('creating classifier %d' % i)
            print ('size of input training data = (%d,%d)' % X_i.shape)
            self.classifiers[i].fit(X_i, y_i)


    def predict(self, X):
        print('predicting test data of size (%d,%d)' % X.shape)
        predictions = np.asarray([clf.predict(X) for clf in self.classifiers]).T
        maj = np.apply_along_axis(lambda x: np.argmax(np.bincount(x)),
                                      axis=1,  arr=predictions.astype('int'))
        return maj


    def predict_proba(self, X):
        predictions = np.asarray([clf.predict_proba(X) for clf in self.classifiers]).T
        neg_probs = np.average(predictions[0], axis=1)
        pos_probs = np.average(predictions[1], axis=1)
        return np.column_stack((neg_probs, pos_probs))


if __name__=='__main__':
    from ML_utils import description_analyzer

    trainfile = 'part_code_description_train.csv'
    label = '31'
    data_description = "sample training data"
    prevalence = 0.5

    svm_args = {'kernel':'linear', 
                'C':100, 
                'probability':True }

    vec_args = {'min_df':2, 
                'lowercase':False, 
                'binary':True, 
                'analyzer':description_analyzer}

    n_classifiers = 10
    sample_size = 0.1


    from sklearn.feature_extraction.text import CountVectorizer
    count_vect = CountVectorizer(**vec_args)

    from create_training_data import load_sampled_data
    train_data = load_sampled_data(trainfile, label, \
                                   description=data_description, \
                                   prevalence=prevalence)
    
    X = count_vect.fit_transform(train_data.data)
    y = train_data.target

    from sklearn import svm
    sc = SamplingClassifier(svm.SVC, svm_args, n_classifiers, sample_size)
    sc.fit(X, y)

    sc.predict(X)