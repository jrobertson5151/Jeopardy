import os
import pickle

from LDA import *
path = 'bbcsport'


docs = []
for (dirpath, dirnames, filenames) in os.walk(path):
    for f_name in filenames:
        with open(dirpath + '/' + f_name, 'r', encoding='latin-1') as txt_file:
            print(dirpath +'/' + f_name)
            data = txt_file.read().replace('\n', ' ')
            docs.append(data)

l = LDA(docs, K = 5)
l.train(n_iterations=100)
l.pickle_LDA('pickledlda')
