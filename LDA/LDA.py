import numpy as np
import ipdb
import pickle
import string

from stopwords import *

def strip_punctuation(doc):
    doc = doc.strip()
    punctuation = [',', '.', '?', ';', ':', '\'', '(', ')',
                   '&', '!', '"', '[', ']', '-']
    return ''.join([ch.lower() for ch in doc if ch not in punctuation])

def tokenize(docs):
    #split into list of words, excluding stopwords
    words = set()
    words_by_appearance = dict()
    edited_docs = []
    for d in docs:
        d = strip_punctuation(d)
        tokenized_d = []
        words_in_d = d.split(' ')
        words_in_d = [word for word in words_in_d if word not in stopwords and len(word) > 1]
        words.update(words_in_d)
        edited_docs.append(words_in_d)
    M = len(docs)
    return (edited_docs, words)
        
def normalize(probs):
    return np.array([p/sum(probs) for p in probs])

class LDA():
    def __init__(self, docs, K, alpha = .1, beta = 1.):
        self.K = K
        self.alpha = alpha
        self.beta = beta

        (self.docs, self.vocab) = tokenize(docs)
        self.V = len(self.vocab)
        
        self.M = len(docs)
        
        self.Nd = np.array([len(docs[i]) for i in range(self.M)])
        self.N = sum(self.Nd)
        
    def train(self, n_iterations = 10):
        def compute_weird_fraction(helper_word, helper_topic_num):
            numerator = word_topic_count[(helper_topic_num, helper_word)] + self.beta
            denominator = topic_count[helper_topic_num] + self.V*self.beta
            return numerator/denominator
            
        guesses = [[np.random.randint(self.K) for i in range(self.Nd[doc_num])]
                   for doc_num in range(self.M)]
        #initialize word_topic_count and topic_doc_count according to guesses
        word_topic_count = dict()
        topic_doc_count = dict()
        topic_count = [0 for k in range(self.K)]

        for word in self.vocab:
            for topic_num in range(self.K):
                word_topic_count[(topic_num, word)] = 0

        for doc_num in range(self.M):
            for topic_num in range(self.K):
                topic_doc_count[(doc_num, topic_num)] = 0
            
        for (doc_num, doc) in enumerate(self.docs):
            for (word_num, word) in enumerate(doc):
                word_topic_count_key = (guesses[doc_num][word_num], word)
                word_topic_count[word_topic_count_key] += 1

                guess = guesses[doc_num][word_num]
                topic_doc_count_key = (doc_num, guess)
                topic_doc_count[topic_doc_count_key] += 1            

                topic_count[guess] += 1
                
        for iteration in range(n_iterations):
            changed_guesses = 0
            for (doc_num, doc) in enumerate(self.docs):
                if doc_num % 20 == 0:
                    print(iteration, doc_num, changed_guesses)
                for (word_num, word) in enumerate(doc):
                    old_topic_guess = guesses[doc_num][word_num]
                    word_topic_count[(old_topic_guess, word)] -= 1
                    topic_doc_count[(doc_num, old_topic_guess)] -= 1
                    topic_count[old_topic_guess] -= 1
                    
                    unnormalized_ps = []
                    for topic_num in range(self.K):
                        weird_fraction = compute_weird_fraction(word, topic_num)
                        other_term = topic_doc_count[(doc_num, topic_num)]+self.alpha
                        unnormalized_ps.append(weird_fraction*other_term)
                    normalized_ps = normalize(unnormalized_ps)
                    new_guess = np.random.choice(self.K, p=normalized_ps)
                    
                    guesses[doc_num][word_num] = new_guess
                    word_topic_count[(new_guess, word)] += 1
                    topic_doc_count[(doc_num, new_guess)] += 1
                    topic_count[new_guess] += 1
                    if new_guess != old_topic_guess:
                        changed_guesses += 1
                        
        self.phi = np.array([[word_topic_count[(topic_num, word)] + self.beta
                              for word in self.vocab]
                             for topic_num in range(self.K)])
        for (row_num, row) in enumerate(self.phi):
            self.phi[row_num] = normalize(row)

        self.theta = np.array([[topic_doc_count[(doc_num, topic_num)] + self.alpha
                                for topic_num in range(self.K)]
                                for doc_num in range(self.M)])
        for (row_num, row) in enumerate(self.theta):
            self.theta[row_num] = normalize(row)

    def key_words(self):
        #return list of K lists of n_words each
        '''
        P(k | w) = P(w | k)*P(k)/P(w)
        = phi[k, w]*sum(phi[k,w])
        '''
        most_likely_topic_by_word = []
        for (word_num, word) in enumerate(self.vocab):
            word_probs = self.phi[:, word_num]
            associated_topic = np.argmax(word_probs)
            prob_of_topic_given_word = word_probs[associated_topic]/word_probs.sum()
            most_likely_topic_by_word.append((word, word_num,
                            associated_topic, prob_of_topic_given_word))

        most_likely_topic_by_word = [[x for x in most_likely_topic_by_word if x[2] == topic]
                                     for topic in range(self.K)]
        for t in range(self.K):
            most_likely_topic_by_word[t].sort(key = lambda tup: tup[3])
        return most_likely_topic_by_word

    def pickle_LDA(self, dest):
        with open(dest, 'wb') as output_file:
            pickle.dump(self, output_file)


def unpickle_LDA(input_loc):
    with open(input_loc, 'rb') as input_file:
        return pickle.load(input_file)
