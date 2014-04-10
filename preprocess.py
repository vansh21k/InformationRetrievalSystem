'''
Created on 10-Apr-2014

@author: VANSH
'''
import re, collections
import string
from stemming.porter2 import stem

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

def removeNonAscii(s): 
    if s is None:
        return ""
    return filter(lambda x: x in string.printable, s)


def correct_sentence(sentence):
    new = ""
    for word in sentence.split():
        new = new +  " " + correct(word)
    return new.strip()

def name_normalizer(s):
    exclude = set(string.punctuation)
    s = ''.join(ch for ch in s if ch not in exclude)
    return s

def removePunctuation(s):
    ''' Removes punctuation for indexing'''
    exclude = set(string.punctuation)
    test = ''
    for each in s:
        if each in exclude:
            test = test + ' '
        else:
            test = test + each
    return " ".join(test.split())