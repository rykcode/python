# /usr/local/bin/python3
# -*- coding: utf-8 -*-

import numpy as np


def description_analyzer(text):
    ''' A scikit learn analyzer to analyze text data.
    Parameters:
        -----------
        text: str 
            The text
    Returns:
        -----------
        generator:
            Returns a generator over the analyzed tokens of the text
    Usage:
        # create a arguments dict for the classifier
        vec_args = {'min_df':2, 'lowercase':False, 'binary':True, 'analyzer':description_analyzer}
        # create a scikit-learn CountVectorizer
        count_vect = CountVectorizer(**vec_args)
        # create the numpy vector matrix from a list of texts
        X = count_vect.fit_transform([
                                        ["The quick brown fox"], 
                                        ["Jumped over the lazy dog"], 
                                        ["This is a test"]
                                    ])
    '''
    import re
    alphare = re.compile('[a-zA-Z]')
    features = set([])
    for comma_item in text.split(','):
        for hyphen_item in comma_item.split(' - '):
            if not alphare.search(hyphen_item):
                continue
            features.add(hyphen_item)
            for space_item in hyphen_item.split():
                if not alphare.search(space_item):
                    continue
                features.add(space_item)
    for item in features:
        item = item.strip().strip(' -').lower()
        if len(item) == 1:
            continue
        yield item


# def get_masked_data(inputdata, mask, description=None):
#     masked_data = np.array(inputdata.data)[mask is True]
#     masked_filenames = np.array(inputdata.filenames)[mask is True]
#     masked_target_names = np.array(inputdata.target_names)[mask is True]
#     masked_target = np.array(inputdata.target)[mask is True]
#     return Bunch(data = masked_data,
#                 filenames = masked_filenames,
#                 target_names = masked_target_names,
#                  target = masked_target,
#                  DESCR = description)


def get_random_mask(mask_size, percent):
    ''' Returns a 1D array of given size consisting of mostly True and randomly marked without replacement False values. 
        Parameters:
            -----------
            mask_size: int
                The size of the mask
            percent: float
                The percentage of values in the resulting array to be set to False
        Returns:
            -------
            mask : 1-D np array
                The mask array containing True and randomly marked False values. 
    '''
    import numpy as np
    mask = np.ones(mask_size, dtype=bool)
    sample_size = int(mask_size * percent)
    sampled = np.random.choice(mask_size, sample_size, replace=False)
    mask[sampled] = False
    return mask


def create_cv_data(train_data, percent):
    ''' Creates input data for cross validation
        Parameters:
        -----------
        train_data: Bunch
                The training data
        percent: float
                The percentage of data to be left out for testing
    '''
    mask = np.ones(train_data.filenames.shape, dtype=bool)
    sample_size = int(mask.shape[0] * percent)
    sampled = np.random.choice(mask.shape[0], sample_size)
    mask[sampled] = False
    train_CV = get_masked_data(train_data, mask, "train split for CV")
    test_CV = get_masked_data(train_data, ~mask, "test split for CV")
    return train_CV, test_CV



def top_features_chi2(X, y):
    feature_scores = chi2(X, y)
    np.histogram(feature_scores[0])
    np.histogram(feature_chi2[0]) >= 6.62727273
    np.array(feature_names)[feature_chi2[0] >= 6.62727273]
    feature_scores = mutual_info_classif(
                            count_vect.fit_transform(
                                train_data.data), train_data.target)
    
    train_data_new = SelectPercentile(mutual_info_classif, 15).fit_transform(count_vect.transform(train_data.data), train_data.target)


def write_dict_to_file(data, filename):
    ''' Given the classifier and CountVectorizer apply it on the
        test_data and write the predictions to the predictions file.
        Parameters:
            -----------
            data: iterable of tuples
                    An iterable of tuples. For ex. the instance_id
                    and corresponding prediction probability
            filename: str
                    The name of the output predictions file
    '''
    import csv
    with open(filename, 'w') as fout:
        writer = csv.writer(fout)
        for item in data:
            writer.writerow(item)
