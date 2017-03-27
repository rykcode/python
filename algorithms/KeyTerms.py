'''
Created on Dec 28, 2013

@author: rohit


'''

import Utils
import nltk
import collections

class KeyTerms():
    def __init__(self):
        pass
    
    def removeNonSensicalNgrams(self, ngrams):
        """ Removes all such ngrams.
        1. Ngram that doesn't start with a noun or adjective
        2. Ngram that doesn't end with a noun or adjective
        3. Ngram that spans sentences or has a comma as one of its elements
        """
        non_sensical_ngrams = set([])
        for ngram in ngrams:
            #check if ngram starts with a noun or adjective
            if not (ngram[0].tag.startswith('JJ') or ngram[0].tag.startswith('NN')):
                non_sensical_ngrams.add(ngram)
                
            #check if ngram ends with a noun or adjective
            if not (ngram[-1].tag.startswith('JJ') or ngram[-1].tag.startswith('NN')):
                non_sensical_ngrams.add(ngram)
                
            #check if ngram spans sentences
            for item in ngram:
                if item.word in (',', '.'):
                    non_sensical_ngrams.add(ngram)
                    break
        #remove all such non-sensical ngrams
        for ngram in non_sensical_ngrams:
            ngrams.pop(ngram)
        
            
    def countNgrams(self, text):
        ngrams = []
        sentences = nltk.sent_tokenize(text)
        words = []
        for sent in sentences:
            words += nltk.word_tokenize(sent)
        print 'split the text into %d words' % len(words)
        tags = nltk.pos_tag(words)
        print 'tagged all the words'
        Word = collections.namedtuple('Word', 'word tag')
        word_tags = [word_tag for word_tag in (Word(w,t) for w,t in tags)]
        ngrams += Utils.find_ngrams(word_tags, 1)
        ngrams += Utils.find_ngrams(word_tags, 2)
        ngrams += Utils.find_ngrams(word_tags, 3)
        print 'number of ngrams found = %d' % len(ngrams)
        ngram_freqs = collections.Counter(ngrams)
        print 'computed ngram freq dict. number of uniq ngrams = %d' % len(ngram_freqs)
        self.removeNonSensicalNgrams(ngram_freqs)
        print 'after removing non-sensical ngrams, number of uniq ngrams = %d' % len(ngram_freqs)
        for item, count in ngram_freqs.iteritems():
            print item, count

if __name__ == '__main__':
    fin = open("9c07e0673567_text.txt")
    text = fin.read().replace('\n', ' ')
    fin.close()
    
    keyterms = KeyTerms()
    keyterms.countNgrams(text)
#     keyterms.get_key_terms(text)
    
    
