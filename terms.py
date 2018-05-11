#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 12:53:28 2018

@author: devon
"""

import pdf_text as pt
import nltk
from nltk.util import ngrams
from nltk.corpus import stopwords
from collections import Counter
import string
import re

stop_words = set(stopwords.words('english'))

if __name__ == "__main__":
    filename = "Collins2012.pdf"
    text = pt.extract_text("papers/" + filename)
    text = text.decode('utf-8').strip().lower()
    for s in string.punctuation: text = text.replace(s, "")
    
    tokens = nltk.word_tokenize(text)
    bigrams = list(ngrams(tokens, 2))
    trigrams = list(ngrams(tokens, 3))
    
    bigrams = [b for b in bigrams if b[0] not in stop_words and b[1] not in stop_words]
    trigrams = [b for b in trigrams if b[0] not in stop_words and b[1] not in stop_words and b[2] not in stop_words]
    
    c = Counter(bigrams)
    print Counter(el for el in c.elements() if c[el] >= 10)
    
    c = Counter(trigrams)
    print Counter(el for el in c.elements() if c[el] >= 5)