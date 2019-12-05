import codecs
import os
import re
import string
from collections import Counter
import pickle
import math
from nltk.corpus import stopwords as sw
import nltk,string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import codecs


def rem_sw(tokens):
    stop_w = set(sw.words('english'))
    # tokens = word_tokenize(text)
    res = [i for i in tokens if i not in stop_w]
    return res


def remove_blank_tokens(tokens):
    non_blank = [w for w in tokens if w]
    return non_blank    

#returns tokens
def word_tokenizer(text):
    # Removed punctuation and then split tokens on the basis of whitespaces
    # table = str.maketrans('', '', string.punctuation)
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    text = text.translate(translator)
    # text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = remove_blank_tokens(tokens)
    tokens = rem_sw(tokens)    
    tokens = lemmatize(tokens)
    return tokens

def read_file(file):
    fp = codecs.open(file, "r", encoding='utf-8', errors='replace')
    # text_w_meta = fp.read()
    lines = fp.readlines()    
    lines = [ l.lower() for l in lines]
    return lines


def lemmatize(tokens)  :
    lemmatizer = WordNetLemmatizer() 
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    return tokens

def store_data(data):
    dbfile = open('array_glove', 'wb')
    pickle.dump(data, dbfile)
    dbfile.close()

def load_data(filename):
    file = open(filename,'rb')
    db = pickle.load(file)
    file.close()
    return db

if __name__ == '__main__':
    '''Comment out'''
    #
    # filename = 'corpus.txt'
    # lines = read_file(filename)
    # array = [word_tokenizer(l) for l in lines ]
    # store_data(array)
    #
    lines = load_data('wiki_database_glove')
    print(lines)

    # print(len(array),array[1])