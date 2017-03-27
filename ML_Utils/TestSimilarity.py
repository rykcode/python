#/usr/local/bin/python
# -*- coding: utf-8 -*-


def read_dict(line):
    lkey = None
    ldict = {}
    splitline = line.split("=")
    if len(splitline) == 2:
        lkey = splitline[0]
    linestr = splitline[-1]
    for item in linestr.split(", "):
        k, v = item.split(":")
        ldict[k] = float(v)
    return lkey, ldict


def compare_dict_with_tolerance(d1, d2):
    keys_are_equal = set(d1.keys()) == set(d2.keys())
    if not keys_are_equal:
        return False
    for k1, v1 in d1.iteritems():
        v2 = d2[k1]
        if abs(v1 - v2) >= 0.000001:
            print k1, v1, v2
            return False
    return True


def get_tfidf_vector(tf_vec, refvec_global_df, num_docs):
    tfidf_vec = {}
    for termid, tf in tf_vec.iteritems():
        df = refvec_global_df[termid]
        idf = math.log(float(num_docs) / df)
        tfidf = tf * idf
        tfidf_vec[termid] = tfidf
    return tfidf_vec


def load_vectors_from_file(filename, findstr="", replacestr=""):
    vectors = {}
    fin = open(filename)
    for line in fin:
        vecid, vec = read_dict(line.strip("\n").replace(findstr, replacestr))
        vectors[vecid] = vec
    fin.close()
    return vectors


vocab_global_file = "vocab_global_vectors"
refvec_global_file = "refvec_global_vectors_before"

fin = open(vocab_global_file)
vocab_global_tf = read_dict(fin.readline().strip("\n").replace("globalTF:", ""))[1]
vocab_global_df = read_dict(fin.readline().strip("\n").replace("GlobalDF:", ""))[1]
fin.close()

fin = open(refvec_global_file)
refvec_global_tf_before = read_dict(fin.readline().strip("\n").replace("referenceTfidf before:", ""))[1]
refvec_global_tf_after = read_dict(fin.readline().strip("\n").replace("referenceTfidf after:", ""))[1]
refvec_global_df = read_dict(fin.readline().strip("\n").replace("globalDF:", ""))[1]
fin.close()

print "read vectors"

assert compare_dict_with_tolerance(vocab_global_tf, refvec_global_tf_before) == True
assert compare_dict_with_tolerance(vocab_global_df, refvec_global_df) == True
print "dicts are in sync."

num_docs = 7
import math

tfidf_computed = get_tfidf_vector(refvec_global_tf_before, refvec_global_df, num_docs)
assert compare_dict_with_tolerance(refvec_global_tf_after, tfidf_computed) == True
print "global vec tfidf computation is correct"

vocab_vectors = load_vectors_from_file("vocab_vectors")
refvec_vectors_before = load_vectors_from_file("refvec_vectors_before")
for vecid, vocab_vec in vocab_vectors.iteritems():
    assert compare_dict_with_tolerance(vocab_vec, refvec_vectors_before[vecid])
print "vocab vectors and ref vectors before are in sync"

refvec_vectors_after = load_vectors_from_file("refvec_vectors_after")
for vecid, tf_vec in refvec_vectors_before.iteritems():
    print "vecid:%s" % vecid
    tfidf_vec = get_tfidf_vector(tf_vec, refvec_global_df, num_docs)
    assert compare_dict_with_tolerance(refvec_vectors_after[vecid], tfidf_vec) == True
print "ref vecs tfidf computation is in sync"
    
