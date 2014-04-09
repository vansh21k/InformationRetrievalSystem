'''
Created on 10-Apr-2014

@author: VANSH
'''
'''
Created on 10-Apr-2014

@author: VANSH
'''
import string
def removePunctuation(s):
    ''' Removes punctuation for indexing'''
    exclude = set(string.punctuation)
    s = ' '.join(ch for ch in s if ch not in exclude)
    return s
