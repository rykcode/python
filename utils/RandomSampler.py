'''
Created on Feb 21, 2013

@author: rohit
'''

'''
randomly sample any column in a delimited file
'''

from optparse import OptionParser
import random

import Utils


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", dest="inputFile", help="input file")
    parser.add_option("-o", dest="outputFile", help="output file")
    parser.add_option("-s", dest="sampleSize", help="sample size")

    (options, args) = parser.parse_args()
    print "input file:%s" % (options.inputFile)
    print "output file:%s" % options.outputFile
    print "sample size:%s" % options.sampleSize

    population = Utils.loadFileAsList(options.inputFile, delim='\t', columntypes=((2, str()),))
    print "size of population:%d" % len(population)
    print population[0:10]
    sample = random.sample(population, int(options.sampleSize))
    Utils.writeToFile(sample, options.outputFile)
