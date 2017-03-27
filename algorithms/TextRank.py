'''
Created on Dec 30, 2013
Implementation based on http://acl.ldc.upenn.edu/acl2004/emnlp/pdf/Mihalcea.pdf
TextRank: Bringing Order into Texts

@author: rohit

'''

import nltk
import collections
from random import randint
import math


class Vertex():
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq
        self.score = 0.1
        self.incoming = {} # incoming vertices and their distances
        self.outgoing = {} # outgoing vertices and their distances
        #in case of undirected graph, incoming and outgoing members will be same.
        self.num_visits = 0 #records the number of times the algorithm visits this vertex
    
    def __str__(self):
        return self.word
#         return "%s, freq:%d, score:%4f, num_visits:%d, incoming:%s, outgoing:%s, num_incoming:%d, num_outgoing:%d" % \
#             (self.word, self.freq, self.score, self.num_visits, sorted(self.incoming.items(), key=lambda (k,v): (v,k), reverse=True), self.outgoing, len(self.incoming), len(self.outgoing)) 
#         return "%s, freq:%d, score:%4f, num_visits:%d, incoming:%s, outgoing:%s" % \
#             (self.word, self.freq, self.score, self.num_visits, self.incoming, self.outgoing) 
#         return "%s, score:%0.4f, num_visits:%d" % (self.word, self.score, self.num_visits)
#         return "%d" % self.num_visits
    
    def increment_num_visits(self):
        self.num_visits += 1

class TextRank():
    def __init__(self):
        self.distance_type = 'exp-decay'
        self.left_window = 3
        self.right_window = 3
        self.damping = 0.85
        #self.num_epochs = 13000        
    
    def get_word_tags(self, text):
        sentences = nltk.sent_tokenize(text)
        words = []
        for sent in sentences:
            words += nltk.word_tokenize(sent)
        print 'split the text into %d words' % len(words)
        tags = nltk.pos_tag(words)
        print 'tagged all the %d words' % len(tags)
        Word = collections.namedtuple('Word', 'word tag')
        word_tags = [word_tag for word_tag in (Word(w,t) for w,t in tags)]
        return word_tags 
    
    def select_vertices(self, word_tags):
        """ Given the word and tags from the text, selects vertices to create an undirected graph
        """
        #TODO: give different scores to NNP, NN and JJ
        self.vertices = {}
        for word in word_tags:
            if self.accept_tag(word):
                if word.word not in self.vertices:
                    self.vertices[word.word] = Vertex(word.word, 0)
                self.vertices[word.word].freq += 1
    
    def accept_tag(self, word):
        """ Accept word if it is a Noun or an adjective
        """
        if word.tag.startswith('NN') or word.tag.startswith('JJ'):
            return True
        return False
    
    def assign_incoming(self, word_tags):
        """ For each vertex, find the incoming vertices and the strengths of the edges.
            Each incoming candidate vertex should be a NN or a JJ and itself be a vertex.
            The strength of edge can be binary or otherwise. 
            Strength is inversely proportional to distance. And distance = num of separating words (not vertices)  
        """
        for i,word in enumerate(word_tags):
            if self.accept_tag(word) is False or word.word not in self.vertices:
                continue
            left_limit = max(0, i-self.left_window)
            #right_limit = min(i+self.right_window, len(word_tags)-1)
            
            #traverse to the left of current word and update incoming vertices
            for j in range(i-1, left_limit-1, -1):
                neighbor = word_tags[j]
                if neighbor.word in set(['.']):#end of sentence. Do not find neighbors across sentences
                    break
                if self.accept_tag(neighbor) is False or \
                    neighbor.word not in self.vertices or \
                        neighbor.word == word.word:
                    continue
                if self.distance_type == 'binary': strength = 1
                elif self.distance_type == 'linear': strength = j - left_limit + 1
                elif self.distance_type == 'exp-decay': strength = math.exp(j-(i-1))
                self.vertices[word.word].incoming[neighbor.word] = strength
            
    def assign_outgoing(self, word_tags):
        """ based on the incoming vertices updates the outgoing vertices.
        """
        for vertex in self.vertices.values():
            for word,strength in vertex.incoming.iteritems():
                incoming_vertex = self.vertices[word]
                incoming_vertex.outgoing[vertex.word] = strength

                            
    def print_vertices(self, sort=False):
        if sort:
            for vertex in sorted(self.vertices.values(), key=lambda x:x.score, reverse=True):
                print vertex
        else:
            for vertex in self.vertices.values():
                print vertex 
    
    def select_random(self, words_list):
        """ Selects a random word from the words_list 
            and returns the corresponding vertex from self.vertices
        """
        rand_word = words_list[randint(0,len(words_list)-1)]
        vertex = self.vertices[rand_word]
        vertex.increment_num_visits()
        return vertex
    
    def update_score(self, vi):
        """ Score of a vertex is influenced by the scores of its incoming vertices and 
            the strength of the link between the vertex and each of its incoming vertex. 
        """
        sum_ = 0.0
        for incoming_word in vi.incoming:
            vj = self.vertices[incoming_word]
            #sum_ += 1./len(vj.outgoing) * vj.score
            vj_vi_strength = vj.outgoing[vi.word]
            sum_outgoing_strengths_vj = sum(vj.outgoing.values())
            sum_ += float(vj_vi_strength) / sum_outgoing_strengths_vj * vj.score
        vi.score = (1-self.damping) + self.damping * sum_

    def random_surf(self):
        """ Surfs the graph. With probability = randomness jumps to a completely random new vertex in the entire graph,
            and with remaining probability randomly jumps to a vertex within the outgoing vertices of the current vertex.
        """
#         initial_learning_rate = 0.7
#         annealing_rate = 0.7
        num_epochs = 20 * len(self.vertices)
        print 'num_epohcs: %d' % num_epochs 
        curr_vertex = self.select_random(self.vertices.keys())
        self.update_score(curr_vertex)
        for epoch in range(1,num_epochs):
            #learning_rate = initial_learning_rate / (1 + float(epoch)/annealing_rate)
#             learning_rate = 0.7
            learning_rate = math.log(float(num_epochs)/epoch, 10) / math.log(num_epochs,10)
            random_jump = float(randint(1,100))/100 < learning_rate
            if random_jump: #select a completely random vertex from the entire set of vertices
                curr_vertex = self.select_random(self.vertices.keys())
                self.update_score(curr_vertex)
            else: # select a random vertex from the outgoing vertices or the current random_vertex
                if not curr_vertex.outgoing:#no outgoing vertices. Hence, select a completely random vertex from the entire set of vertices
                    curr_vertex = self.select_random(self.vertices.keys())
                    self.update_score(curr_vertex)
                else:
                    curr_vertex = self.select_random(curr_vertex.outgoing.keys())
                    self.update_score(curr_vertex)

    def dampen_volume(self):
        """ Reduces the score of a vertex that has high score only because it appears with a lot of other vertices.
            For ex. the word "people" is a NN and appears with a variety of words. So dampen it. 
        """
        for vertex in self.vertices.values():
            if vertex.incoming:
                vertex.score /= len(vertex.incoming)
        
    def run(self, input_val):
        if type(input_val) == type(''):
            word_tags = self.get_word_tags(input_val)
        else:
            word_tags = input_val
        print 'number of word_tags = %d' % len(word_tags)
        self.select_vertices(word_tags)
        print 'number of vertices selected = %d' % len(self.vertices)
        self.assign_incoming(word_tags)
        self.assign_outgoing(word_tags)
        #self.print_vertices(sort=True)
        self.random_surf()
        #self.dampen_volume()
        self.print_vertices(sort=True)

def load_tagged_text(filename):
    word_tags = []
    Word = collections.namedtuple('Word', 'word tag')
    with open(filename) as fin:
        for line in fin:
            w,t = line.strip('\n').split('|')
            word_tags.append(Word(w,t))
    return word_tags

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

    #directly give word_tags as input to save the tagging time
#     word_tags = load_tagged_text("9c07e0673567_text_tagged.txt")
#     tr = TextRank()
#     tr.run(word_tags)
    
    #input is text. This adds to the tagging time of the program.
#     filename = "9c07e0673567_text.txt"
#     filename"text_rank_sample.txt"
    filename = "MachineLearning.txt"
    text = open(filename).read().replace('\n', ' ').replace('&#39;','')
    tr = TextRank()
    tr.run(text)
