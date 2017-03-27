import random

import numpy


class LDA:
    def __init__(self, documents):
        self.documents = documents
        self.words = self.extract_words()
        #print self.words
        self.nd = len(self.documents) # num of docs
        self.nw = len(self.words) # num of words
        self.nt = 2 #num of topics
        self.word_doc_matrix = self.init_word_doc_matrix()
        #print word_doc_matrix
        self.topics = self.init_topics()
        self.topic_assignments = self.random_topic_assignment()
        #print "topic assignments:"
        #print topic_assignments
        self.word_topic_matrix = numpy.zeros((self.nw, self.nt)) # topic-word matrix. rows=words, cols=topics
        self.update_topic_word_matrix()
        #print self.word_topic_matrix
        #print self.word_topic_matrix.sum(axis=0)
        self.topic_doc_matrix = numpy.zeros((self.nd, self.nt)) # topic-doc matrix. rows=docs, cols=topics
        self.update_topic_doc_matrix()

        self.print_topic_words(5)
        self.print_document_topics()

        print "============================= initialization done =============================="

    def print_document_topics(self):
        print "printing topic distribution in each document"
        print self.topic_doc_matrix
        print "==================================\n"

    def print_topic_words(self, topN):
        """ prints top N words for each topic """
        print "printing top words in each topic"
        id2word = dict([(v, k) for k, v in self.words.iteritems()])
        for word_dist in self.word_topic_matrix.T:
            word_ids = word_dist.argsort()[-topN:][::-1]
            print word_dist, sum(word_dist)
            print [id2word[word_id] for word_id in word_ids]
        print "==================================\n"

    def update_topic_doc_matrix(self):
        for docid, docrow in enumerate(self.topic_assignments.T):
            topic_dist = numpy.bincount(docrow)
            norm_topic_dist = topic_dist / float(sum(topic_dist))
            #print docid, docrow, topic_dist, norm_topic_dist
            self.topic_doc_matrix[docid] = norm_topic_dist

    def update_topic_word_matrix(self):
        #print "updating topic word dist"
        for wordid, wordrow in enumerate(self.topic_assignments):
            word_dist = numpy.bincount(wordrow)
            #print word_dist
            #print wordid, wordrow, word_dist
            for topicid, occurrence in enumerate(word_dist):
                self.word_topic_matrix[wordid, topicid] = occurrence
            # normalize word_topic_matrix
        col_sums = self.word_topic_matrix.sum(axis=0)
        self.word_topic_matrix /= col_sums

    def random_topic_assignment(self):
        topic_assignments = numpy.zeros((self.nw, self.nd),
                                        dtype='int64') # a term doc matrix that holds the topic assignments
        # randomly initialize the topic assignments
        for (x, y), value in numpy.ndenumerate(topic_assignments):
            topic_assignments[x, y] = random.randint(0, len(self.topics) - 1)
        return topic_assignments

    def init_topics(self):
        topics = 1. / self.nt * numpy.ones(self.nt) # all topics have equal prob.
        return topics

    def init_word_doc_matrix(self):
        tdmatrix = numpy.zeros((self.nw, self.nd), dtype='int64') # term-document matrix. rows=terms, cols = docs
        for docid, document in enumerate(self.documents):
            docterms = document.split()
            for term in docterms:
                termid = self.words[term]
                tdmatrix[termid, docid] += 1
        return tdmatrix

    def extract_words(self):
        wordset = set([])
        for document in self.documents:
            wordset.update(set(document.split()))
        return dict([[val, idx] for idx, val in enumerate(wordset)])

    def run(self):
        for i in range(0, 10):
            #reassign topics to each word in each document
            # Prob of reassignment = P(t|w,d) = P(t|d) P(w|t)
            for (wordid, docid), value in numpy.ndenumerate(self.word_doc_matrix):
                p_topics = numpy.zeros(self.nt)
                for topicid in range(0, self.nt):
                    #using 1+value as a smoothing technique to avoid divide by zero
                    p_topic_given_word = (1 + value) * self.word_topic_matrix[wordid, topicid] * self.topic_doc_matrix[
                        docid, topicid]
                    p_topics[topicid] = p_topic_given_word
                p_topics /= sum(p_topics) #normalize the probabilities
                #select a random topic based on the topic probabilities
                cumprob = numpy.cumsum(p_topics)
                rand_num = random.randint(0, 100) / 100.01
                new_topic = numpy.searchsorted(cumprob, rand_num)
                self.topic_assignments[wordid, docid] = new_topic
                if new_topic > 1:
                    print "new topic is greater than 1", p_topics, cumprob, rand_num, new_topic
                    break

            self.update_topic_word_matrix()
            self.update_topic_doc_matrix()
            self.print_topic_words(5)
            self.print_document_topics()


if __name__ == '__main__':
#     documents = ["I like to eat broccoli and bananas",\
#              "I ate a banana and spinach smoothie for breakfast",\
#              "Dogs and kittens are cute",\
#              "My sister adopted a kitten yesterday",\
#              "Look at this cute hamster munching on a piece of broccoli",]
    documents = ["like eat broccoli banana", \
                 "ate banana spinach smoothie breakfast", \
                 "Dogs kittens cute", \
                 "sister adopted kitten yesterday", \
                 "cute hamster munching piece broccoli", ]
    lda = LDA(documents)
    lda.run()
    





        