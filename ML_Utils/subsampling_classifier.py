#/usr/local/bin/python3
# -*- coding: utf-8 -*-

''' 
A better version of the Sampleing classifier using pandas. Creates an SVM classifier to subsample a low prevalence labeled dataset. Use Sub-sampling to balance out the prevalence of the labeled data and create several classifiers.
'''
import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
# import sklearn.metrics as metrics


def load_data(filename):
    data = pd.read_csv(filename, sep=',', nrows=1)
    data.columns.values
    dtype_dict = dict([(item, bool) for item in data.columns.values])
    str_columns = ['instance_id', 'label', 'short_description']
    for item in str_columns:
        dtype_dict[item] = str
    data = pd.read_csv(filename, sep=',', dtype=dtype_dict)
    return data


def create_classifiers(train_data):
    positive_instance_ids = np.array(
        train_data[train_data['label'] == label]['instance_id'].tolist())
    negative_instance_ids = np.array(
        train_data[train_data['label'] != label]['instance_id'].tolist())
    negative_lists = [np.random.choice(
        negative_instance_ids, len(positive_instance_ids))
        for i in range(0, 10)]

    clfs_text = [svm.SVC(**svm_args_text) for i in range(0, 10)]
    clfs_cat = [svm.SVC(**svm_args_cat) for i in range(0, 10)]

    print ('starting subsampling')
    for i in range(0, 10):
        train_i = np.concatenate([positive_instance_ids, negative_lists[i]])
        print('iter: %d' % i)
        X_train_i = count_vect.transform(train_data[train_data.instance_id.isin(train_i)]['short_description'])
        y_i = train_data[train_data.instance_id.isin(train_i)]['label'] == label
        print('obtained X_train_%d and y_%d' % (i,i))
        clfs_text[i].fit(X_train_i, y_i)
        print('trained text classifier %d' % i)
        X_train_cat_i = train_data[train_data.instance_id.isin(train_i)].drop(['instance_id', 'label', 'short_description'], axis=1)
        print('obtained X_train_cat_%d and y_%d X_train_cat_i = (%d,%d)' % (i,i, X_train_cat_i.shape[0], X_train_cat_i.shape[1]))
        clfs_cat[i].fit(X_train_cat_i, y_i)
        print('trained category classifier %d' % i)

    return clfs_text, clfs_cat


def predict(data, clfs_text, clfs_cat, out_filename):
    X_text = count_vect.transform(data['short_description'])
    X_cat = data.drop(['instance_id', 'label', 'short_description'], axis=1)
    print('obtained data')

    predictions_text = [clfs_text[i].predict_proba(X_text)[:, 1] for i in range(0, 10)]
    mean_predictions_text = np.mean(predictions_text, axis=0)
    data['text_predictions'] = mean_predictions_text.tolist()
    print('obtained text predictions')

    predictions_cat = [clfs_cat[i].predict_proba(X_cat)[:, 1] for i in range(0, 10)]
    mean_predictions_cat = np.mean(predictions_cat, axis=0)
    data['cat_predictions'] = mean_predictions_cat.tolist()
    print('obtained category predictions')

    data[['instance_id', 'text_predictions', 'cat_predictions']].to_csv(
        out_filename, index=False)

    print('output written to csv')


    
if __name__=='__main__':

    train_file = sys.argv[1]
    test_file = sys.argv[2]
    label = sys.argv[3]

    svm_args_text = {'kernel':'rbf', 'C':100, 'probability':True}
    svm_args_cat = {'kernel':'rbf', 'C':10, 'probability':True}

    print('started')

    train_data = load_data(train_file)
    print('loaded train data %d' % len(train_data))
    test_data = load_data(test_file)
    print('loaded test data %d' % len(test_data))

    count_vec_args = {'min_df':2, 'lowercase':True, 'binary':True,}
    count_vect = CountVectorizer(**count_vec_args)
    count_vect.fit(train_data['short_description'])

    
    clfs_text, clfs_cat = create_classifiers(train_data)

    predict(test_data, clfs_text, clfs_cat, 'preds_test_%s.csv' % label )

    predict(train_data, clfs_text, clfs_cat, 'preds_train_%s.csv' % label )

