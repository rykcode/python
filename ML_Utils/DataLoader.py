#/usr/local/bin/python3
# -*- coding: utf-8 -*-

'''

@author: rohit
'''

import csv
import numpy as np

class TextFileData:
    '''
        Loads all the data from the text file in to this object.
    '''
    def __init__(self, input_filename, train_mode=True, instance_ids_to_keep=None, instance_ids_to_ignore=None, positive_label=None, load_texts=False, skip_rows_with_terms=None):
        self.train_mode = train_mode
        self.input_filename = input_filename
        self.load(instance_ids_to_keep=instance_ids_to_keep, instance_ids_to_ignore=instance_ids_to_ignore, positive_label=positive_label, load_texts=load_texts, skip_rows_with_terms=skip_rows_with_terms)



    def load(self, instance_ids_to_keep=None, instance_ids_to_ignore=None, positive_label=None, load_texts=False, skip_rows_with_terms=None):
        ''' Loads the training or testing text file in to this object. The attributes available are instance_ids, labels, texts.
        Parameters:
            -----------
            instance_ids_to_keep: numpy array (Default None)  
                The instance ids to load. If provided then all instance ids NOT present in this array are ignored.
            instance_ids_to_ignore: numpy array (Default None)  
                The instance ids to ignore. If provided then all instance ids present in this array are ignored.
            positive_label: str (Default None)
                The positive label. If provided then all positive labels are loaded as 1 and remaining labels are loaded as 0 in this object's target attribute.
            load_texts: boolean (Default False)
                Whether or not to load the texts from the file.
        Returns:
            -------
            Returns nothing. All relevant data is loaded in to the object.
        Usage:
            -------
            load training data as follows
                train_data = TextFileData(trainfile, train_mode=True, instance_ids_to_keep=train_ids, positive_label=label, load_texts=False, skip_rows_with_terms=skip_rows_with_terms)
            load holdout data as follows
                ho_data = TextFileData(trainfile, train_mode=True, instance_ids_to_keep=holdout_ids, positive_label=label, load_texts=True, skip_rows_with_terms=skip_rows_with_terms)
            load test data as follows
                test_data = TextFileData(testfile, train_mode=False, load_texts=True, skip_rows_with_terms=skip_rows_with_terms)

        '''
        instance_ids = []
        labels = []
        texts = [] if load_texts else None
        nodescription = nodescription_positive = 0
        with open(self.input_filename) as fin:
            reader = csv.DictReader(fin, delimiter=",", quotechar='"', skipinitialspace=True)
            for row in reader:
                instance_id = row['instance_id']

                if instance_ids_to_keep is not None and instance_id not in instance_ids_to_keep:
                    continue

                if instance_ids_to_ignore is not None and instance_id in instance_ids_to_ignore:
                    continue

                text = row['short_description'].strip()

                skip_row = False
                lower_text = text.lower()
                for item in skip_rows_with_terms:
                    if item in lower_text:
                        skip_row = True
                        break
                if skip_row:
                    continue

                if len(text) == 0:
                    if self.train_mode and row['label'] == positive_label:
                        nodescription_positive += 1
                    nodescription += 1
                    continue

                if self.train_mode:
                    if row['label'] == positive_label:
                        labels.append(1)
                    else:
                        labels.append(0)
                
                instance_ids.append(instance_id)

                if load_texts:
                    texts.append(text)
                
        self.instance_ids = np.array(instance_ids)
        self.target = np.array(labels)
        self.texts = texts


    def get_texts(self):
        ''' Iterate over the texts. Requires that the load method be called. If texts have been previsously loaded then iterate over the in-memory texts present in self.texts else open the file again and iterate over the texts.
        '''
        nodescription = nodescription_positive = 0

        if hasattr(self, 'texts') and self.texts is not None:
            for text in self.texts:
                yield text
        else:
            instance_id_set = set(self.instance_ids)
            with open(self.input_filename) as fin:
                reader = csv.DictReader(fin, delimiter=",", quotechar='"', skipinitialspace=True)
                for row in reader:

                    instance_id = row['instance_id']
                    if instance_id not in instance_id_set:
                        continue

                    text = row['text'].strip()
                    yield text


    def fill_features(self, count_vect, X):
        self.features = [None]*X.shape[0]
        feature_names = np.array(count_vect.get_feature_names())
        for i in range(0,X.shape[0]):
            features_i = feature_names[np.nonzero(X[i,:])[1]]
            # feature_i_str = ','.join(features_i)
            self.features[i] = features_i

    def fill_features_as_array(self, count_vect, X):
        self.features = np.empty([X.shape[0],1], dtype='<U100')
        feature_names = np.array(count_vect.get_feature_names())
        for i in range(0,X.shape[0]):
            features_i = feature_names[np.nonzero(X[i,:])[1]]
            feature_i_str = ','.join(features_i)
            self.features[i] = feature_i_str


    