'''
Created on Jan 16, 2014

This is anti TF-IDF. 
Split the given text in to paragraphs.
Analyze a paragraph and compute
1. Within paragraph freq - infreq
2. Outside paragraph freq - outfreq

There are 4 possibilities
1. infreq is high and outfreq is high - these are fluff words
2. infreq is high and outfreq is low - these are unique to the paragraph but not to the document
3. infreq is low and outfreq is high - these are unique to some other paragraph so not useful in this paragraph
4. infreq is low and outfreq is low - these are sparingly mentioned in this paragraph and the rest of the document. 
These are interesting words. They are not too common to be fluff words yet are referenced in the rest of the document.

So the order of importance is 4,2,3,1
For this one possible scoring measure is 1/infreq * 1/outfreq
To avoid divide by zero we could do smooth. 

@author: rohit

'''

import nltk
import collections

WordTag = collections.namedtuple('WordTag', 'word tag')#A named tuple for storing word and its tag with names [word, tag]

class ImportantTermsInParagraphs():
    def __init__(self):
        pass
    
    def get_tokenized_sentences(self, sentences):
        return [nltk.word_tokenize(sent) for sent in sentences]
    
    def get_tagged_sentences(self, sentences):
        """ Given the text returns the 
        [[[word_tag, word_tag, ...], [word_tag, word_tag, ...], [word_tag, word_tag, ...]]"""
        #WordTag = collections.namedtuple('WordTag', 'word tag')#declare the named tuple with names [word, tag]
        tagged_sentences = []
        for sent in sentences:
            tags = nltk.pos_tag(nltk.word_tokenize(sent))
            tagged_sentences.append([WordTag(w,t) for w,t in tags])
        return tagged_sentences
            
    def get_counts(self, tagged_sentences):
        global_counts = collections.Counter()
        for tagged_sent in tagged_sentences:
            for word_tag in tagged_sent:
                if word_tag.tag.startswith("NN") or word_tag.tag.startswith("JJ"):
                    try: global_counts[word_tag] += 1
                    except KeyError: global_counts[word_tag] = 1
        return global_counts
    
    def get_scores(self, local_counts, global_counts):
        scores = {}
        for word, infreq in local_counts.iteritems():
            outfreq = global_counts.get(word) - infreq
            if outfreq == 0: score = 0 
            elif infreq == outfreq == 1: score = 0 
            #else: score = 1.0/(infreq * outfreq)
            else: score = float(infreq + outfreq)/(infreq * outfreq)
            scores[word] = score
        return scores 
    
    def get_keywords(self, text):
        window = 5
        sentences = nltk.sent_tokenize(text)
        tagged_sentences = self.get_tagged_sentences(sentences)
        global_counts = self.get_counts(tagged_sentences)
#         for k,v in sorted(global_counts.items(), key=lambda (k,v) : (v,k), reverse=True):
#             print k,v
        best_scores = {}
        best_values = {}
        for i in range(0,len(tagged_sentences)-window):
            paragraph = tagged_sentences[i:i+window]
            local_counts = self.get_counts(paragraph)
            para_scores = self.get_scores(local_counts, global_counts)
            for word,infreq in local_counts.iteritems():
                score = para_scores[word]
                if score == 0: continue
                curr_score = best_scores.get(word, 0)
                if score > curr_score:
                    best_scores[word] = score
                    outfreq = global_counts[word] - infreq
                    best_values[word] = [infreq, outfreq]
        print "========================= final scores ========================="
        for word, score in sorted(best_scores.items(), key=lambda (k,v):(v,k)):
            print word.word#, score, best_values[word]
        

if __name__ == '__main__':
    tr = ImportantTermsInParagraphs()
    filename = "9c07e0673567_text.txt"
    
    tr.get_keywords(open(filename).read().replace('\n', ' ').replace('&#39;',''))
    
    
    
    
