""" Filter the contents of a file using another file.
"""

import argparse
import Utils


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate the accuracy of each bucket')
    parser.add_argument("-m", "--mode", dest="mode", help="modes = [keep, ignore, range]")
    parser.add_argument("-i", "--inputFile", dest="inputFile", help="The input file")
    parser.add_argument("-f", "--filterFile", dest="filterFile", help="The filter file")
    parser.add_argument("-r", "--filterRange", dest="filterRange", help="The low,high range to retain")
    parser.add_argument("-o", "--outputFile", dest="outputFile", help="The output filtered file")

    args = parser.parse_args()

    outlist = []
    inputdocs = Utils.loadFileAsList(args.inputFile, columntypes=((0, int()), (2, float()),), delim='\t')
    if args.mode == 'range':
        low, high = map(float, args.filterRange.split(','))
        for docid, neg in inputdocs:
            if low <= neg < high:
                outlist.append(docid)
    print 'len outlist:%d' % len(outlist)

    # filterdocs = set(Utils.loadFileAsList(args.filterFile, columntypes=((0,str()), )))
    # outlist = []
    # for a,b in inputdocs:
    # 	if a not in filterdocs:
    # 		outlist.append(a + '\t' + b)
    fout = open(args.outputFile, 'w')
    fout.write('\n'.join(map(str, outlist)))
    fout.close()

