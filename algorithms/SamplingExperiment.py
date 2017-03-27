"""experiment to find which is better
1. estimate from a single sample from a large distribution OR 
2. estimate from several samples from a large distribution  

@author: rohit

"""

import random

import numpy as np


def generateData(n, p, s, datafile):
    """generate binomially distributed data and write to file
    """
    data = np.random.binomial(n, p, s)
    fout = open(datafile, 'w')
    fout.write('\n'.join(map(str, data)))
    fout.close()


def singleSample(data, samplesize):
    """draw a sample from the data and return the proportion of 1's
    """
    rand_indices = random.sample(xrange(len(data)), samplesize)
    sum = 0
    for index in rand_indices:
        sum += data[index]
    proportion = float(sum) / samplesize
    #     print "sum =", sum, ", proportion =", proportion
    return proportion


def singleSampleExperiment(datafile, samplesize):
    fin = open(datafile)
    data = map(int, fin.read().split('\n'))
    fin.close()
    return singleSample(data, samplesize)


def multipleSamplesExperiment(datafile, total_samplesize, num_samples):
    samplesize = total_samplesize / num_samples

    #     print 'total sample size =', total_samplesize
    #     print 'individual samplesize =', samplesize

    fin = open(datafile)
    data = map(int, fin.read().split('\n'))
    fin.close()
    sampling_dist = []
    for i in range(num_samples):
        prop = singleSample(data, samplesize)
        sampling_dist.append(prop)
    print sampling_dist
    mean = float(sum(sampling_dist)) / num_samples
    #     print mean
    return mean


if __name__ == '__main__':
    datafile = 'random_binom_data.txt'
    #     n, p, s = 1, 0.1, 100000 #num trials, p-value of binom dist, num samples to generate
    #     generateData(n, p, s, datafile)
    #     print "generated data file"

    count = 0
    for i in range(1):
        total_samplesize = 500
        #     print 'single sample experiment'
        single_prop = singleSampleExperiment(datafile, total_samplesize)
        #     print 'samplesize =', total_samplesize
        #     print 'proportion =', single_prop

        num_samples = 10
        #     print 'multiple samples experiment'
        sampling_proportion = multipleSamplesExperiment(datafile, total_samplesize, num_samples)
        print single_prop, sampling_proportion, abs(single_prop - 0.995) > abs(sampling_proportion - 0.995)
        if abs(single_prop - 0.995) > abs(sampling_proportion - 0.995): count += 1
    print count
    
    
    