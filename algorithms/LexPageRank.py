'''
Created on Dec 30, 2013

Based on the paper
LexPageRank: Prestige in Multi-Document Text Summarization
link = http://acl.ldc.upenn.edu/acl2004/emnlp/pdf/Erkan.pdf

This algorithm creates sentence summaries of texts. 
The summaries are created from N top most prestigious sentences in the document.
The prestige computation is an adaptation of pagerank algorithm to text sentences.

@author: rohit

TODO: ideas 
1. Introduce some kind of tfidf influence in order to weigh words. Currently "people" seems to be the most common word
and because all words are weighed equally it dominates the similarity
2. Give more weights to words that are part of NNP or phrases. This will reduce the influence of words like people etc.  
'''

import nltk
import collections
import numpy
import math


WordTag = collections.namedtuple('WordTag', 'word tag')#A named tuple for storing word and its tag with names [word, tag]
Feature = collections.namedtuple('Feature', 'id weight')#A named tuple for storing features with names [id, weight]

class LexPageRank():
    def __init__(self):
        pass
    
    def get_tagged_sentences(self, sentences):
        """ Given the text returns the 
        [[[word_tag, word_tag, ...], [word_tag, word_tag, ...], [word_tag, word_tag, ...]]"""
        #WordTag = collections.namedtuple('WordTag', 'word tag')#declare the named tuple with names [word, tag]
        tagged_sentences = []
        for sent in sentences:
            tags = nltk.pos_tag(nltk.word_tokenize(sent))
            tagged_sentences.append([WordTag(w,t) for w,t in tags])
        return tagged_sentences
    
    def get_features(self, tagged_sentences):
        """ selects all NN and JJ to create the features """
        features = {}
        idx = 0
        for tagged_sent in tagged_sentences:
            for word_tag in tagged_sent:
                weight = None
                if word_tag.tag.startswith('NNP'):
                    weight = 10
                elif word_tag.tag.startswith('NN'):
                    weight = 1
                elif word_tag.tag.startswith('JJ'):
                    weight = 1
                if weight:
                    if word_tag not in features:
                        features[word_tag] = Feature(idx, weight)
                        idx += 1
        return features
    
    def get_vocab_all(self, tagged_sentences):
        """ selects all words except stopwords create the vocab """
        with open('stopwords.txt') as fin:
            text = fin.read()
            stopwords = set(text.split('\n')) 
        
        vocab = {}
        idx = 0
        for tagged_sent in tagged_sentences:
            for word_tag in tagged_sent:
                if word_tag.word.lower() not in stopwords:
                    if word_tag not in vocab:
                        vocab[word_tag] = idx
                    idx += 1
        return vocab
    
    def get_vectors(self, tagged_sentences, features):
        """ returns vectors representation of the tagged_sentences given the features"""
        vectors = []
        for tagged_sent in tagged_sentences:
            vector = {}
            for word_tag in tagged_sent:
                feature = features.get(word_tag)
                if feature:
                    vector[word_tag] = feature.weight
            vectors.append(vector)
        return vectors
    
    def get_similarity(self, pov_vector, target_vector):
        """ return the similarity between the two sentence vectors
            similarity = a_i * b_i / (sqrt(a_i*ai) * sqrt(b_i*b_i)) """
        if not (pov_vector and target_vector):
            return 0.0 
        num_sum = pv_mag = tv_mag = 0
        for pk, pv in pov_vector.iteritems():
            tv = target_vector.get(pk)
            if tv:
                num_sum += pv * tv
        for pv in pov_vector.values():
            pv_mag += pv * pv
        pv_mag = math.sqrt(pv_mag)
        for tv in target_vector.values():
            tv_mag += tv * tv
        tv_mag = math.sqrt(tv_mag)
        sim = num_sum / (pv_mag * tv_mag)
        return sim
    
    def get_similarity_matrix(self, vectors):
        """ returns the N x N similarity matrix of the sentence vectors"""
        N = len(vectors)
        sim_matrix = numpy.matrix(numpy.zeros(shape=(N,N)))
        for i,pov_vector in enumerate(vectors):
            for j,target_vector in enumerate(vectors):
                if i == j: score = 1.0
                else: score = self.get_similarity(pov_vector, target_vector)
                sim_matrix[i,j] = score
        return sim_matrix 
    
    def get_adjacency_matrix(self, sim_matrix):
        """ create a new matrix which is a discretized form of the sim_matrix above a certain threshold """
        adj_matrix = numpy.matrix(numpy.zeros(shape=sim_matrix.shape))
        for i in range(sim_matrix.shape[0]):
            for j in range(sim_matrix.shape[1]):
                if sim_matrix[i,j]>=0.2: adj_matrix[i,j] = 1
        return adj_matrix
    
    def row_normalize(self, adj_matrix):
        """ normalize such that sum of each row of the matrix equals 1"""
        row_sums = adj_matrix.sum(axis=1)
        adj_matrix = adj_matrix / row_sums
        return adj_matrix
    
    def run_page_rank(self, adj_matrix, d=0.85):
        num_sent = adj_matrix.shape[0]
        curr_sent_ranks = numpy.matrix(numpy.zeros(shape=(1,num_sent)))
        new_sent_ranks = numpy.matrix(1.0 / num_sent * numpy.ones(shape=(1,num_sent)))# a 1 x n matrix for sentence rank
        for i in range(500):
            curr_sent_ranks = new_sent_ranks
            #print "curr_sent_ranks", type(curr_sent_ranks)
            #print curr_sent_ranks
            new_sent_ranks = (1-d)/num_sent * numpy.ones(shape=(1,num_sent)) + d * curr_sent_ranks * adj_matrix
        return new_sent_ranks
    
    def generate_summary(self, text):
        sentences = nltk.sent_tokenize(text)
        print "num sentences: %d" % len(sentences)
        tagged_sentences = self.get_tagged_sentences(sentences)
        print "num tagged sentences: %d" % len(tagged_sentences)
        features = self.get_features(tagged_sentences)
        print "size of features: %d" % len(features)
#         for k,v in sorted(features.items(), key=lambda (k,v):(v,k)):
#             print k,v
        vectors = self.get_vectors(tagged_sentences, features)
        print "num vectors: %d" % len(vectors)
#         for vector in vectors:
#             print vector
        sim_matrix = self.get_similarity_matrix(vectors)
        print "sim_matrix:", type(sim_matrix)
#         print sim_matrix
#         for i in [156,144,35,150,76,33,77,86,90,113]:
#             print sentences[i]
#             print ','.join(map(str,sim_matrix[i,]))

        adj_matrix = self.get_adjacency_matrix(sim_matrix)
        print "before normalization, adj_matrix:", type(adj_matrix)
        adj_matrix = self.row_normalize(adj_matrix)
        print "after normalization, adj_matrix:", type(adj_matrix)
        sent_ranks = self.run_page_rank(adj_matrix)
#         print "sent_ranks:", type(sent_ranks)
#         print sent_ranks
        sent_scores = dict([(sent_id,sent_score[0,0]) for sent_id,sent_score in enumerate(sent_ranks.T) ])
        for k,v in sorted(sent_scores.items(), key=lambda (k,v):(v,k), reverse=True):
            #print k,v, sentences[k], vectors[k]
            print sentences[k]
    
    
if __name__ == '__main__':
    ## print the text of the file.
#     fin = open("9c07e0673567_text.txt")
#     text = fin.read().replace('\n', ' ').replace('&#39;','')
#     fin.close()
#     print text

# #     create the word_tags file to save on the tagging time.
#     fin = open("9c07e0673567_text.txt")
#     text = fin.read().replace('\n', ' ').replace('&#39;','')
#     fin.close()
#     tr = TextRank()
#     word_tags = tr.get_word_tags(text)
#     with open("9c07e0673567_text_tagged.txt", "w") as fout:
#         for word in word_tags:
#             fout.write(word.word + "|" + word.tag + "\n")

    #input is text. This adds to the tagging time of the program.
    #fin = open("9c07e0673567_text.txt")
#     fin = open("text_rank_sample.txt")
#     text = fin.read().replace('\n', ' ')
#     fin.close()
#     tr = CustomScoring()
#     tr.generate_summary(text)
    tr = LexPageRank()
    filename = "MachineLearning.txt"
    tr.generate_summary(open(filename).read().replace('\n', ' ').replace('&#39;',''))
    
    
    
    
