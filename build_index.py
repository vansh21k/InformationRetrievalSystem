'''
Created on 10-Apr-2014

@author: VANSH
'''
from stemming.porter2 import stem
import string
from operator import itemgetter
from preprocess import *
global index
global inverted_index
global distinct_words
global index_map
global inverted_index_list
inverted_index_list = []
index_map = {}
index = {} #2d term Frequence Matrix
inverted_index = {} #Inverted Index
distinct_words = set() #Set to identify all words 
n_gram_index = {} # Key: bigram, Value: List of terms 
boolean_inverted_index = [] #Boolean index to support wild card queries and phrasal queries
index_map_inverted = {}
def ngrams_sentence( n_input,n = 2):
    global n_gram_index
    print "In the making for this sentence: " , correct_sentence(removePunctuation(n_input.lower())).strip()
    for each in correct_sentence(removePunctuation(n_input.lower())).strip().split():
        ngrams(each, n)
        print n_gram_index
    
def ngrams(n_input, n = 2):
    print "Current word is", n_input
    global n_gram_index
    orig = n_input
    test = []
    n_input = '%' + n_input + '%' 
    # % used as start/end symbol here
    for each in n_input:
        test.append(each)
    n_input = test
    for i in range(len(n_input)-n+1):
        g = ''.join(n_input[i:i+n])
        if g in n_gram_index:
            n_gram_index[g].append(orig)
        else:
            n_gram_index[g] =[orig]
    
def getName(i):
    global index_map
    for name, counter in index_map.items():
        if counter == i:
            return name
    return None
def buildNGramIndex(file_list,n = 2):
    global n_gram_index
    for each in file_list:
        try:
            with open(each , 'r') as current_file:
                for each_line in current_file:
                    ngrams_sentence(each_line, n)
        except Exception as err:
            print "File Error: " + str(err) 
    print n_gram_index
def buildInvertedIndex():
    ''' Generate the inverted index'''
    global index
    global distinct_words
    global index
    global index_map
    global inverted_index_list
    global boolean_inverted_index
    inverted_index_list = [[0 for x in range(len(index_map))] for y in range(len(distinct_words))]
    for each_word in distinct_words:
        inverted_index[each_word] = []
        for i in range(len(index)):
            each_row = index[i]
            try:
                if each_row[distinct_words.index(each_word)] > 0:
                    inverted_index[each_word].append([getName(i), each_row[distinct_words.index(each_word)]]) 
            except Exception as err:
                print "Unknown Error: " + str(err)
    for each in inverted_index:
        inverted_index[each].sort(reverse = True, key = itemgetter(1,0))
    print inverted_index
    for i in range(len(distinct_words)):
        each = distinct_words[i]
        for each_row in inverted_index[each]:
            if each_row != []:
                inverted_index_list[i][index_map[each_row[0]]]+=each_row[1]
    print "Now giving Inverted Index list"
    print inverted_index_list
    for each in inverted_index_list:
        temp = []
        for each_list in each:
            if each_list > 0:
                temp.append(1)
            else:
                temp.append(0)
        boolean_inverted_index.append(temp)
    print "The boolean invertedL: "
    print boolean_inverted_index

def readFiles(file_list, stemming = False, n = 2):
    '''Read the files, apply normalization and make the files ready for indexing
       Current Standard of Normalization: lower case, remove punctuation, spell check
       To add: Stop Word List
     '''
    global index
    global inverted_index
    global distinct_words
    global index_map
    global index_map_inverted
    count = 0
    for each in file_list:
        try:
            with open(each, 'r') as current_file:
                index_map[each] = count
                for current_line in current_file:
                    current_line = correct_sentence(removePunctuation(current_line.lower())).split(' ')
                    for each_word in current_line:
                        if each_word == '':
                            continue
                        elif stemming == True:
                            distinct_words.add(stem(each_word))
                        else:
                            distinct_words.add(each_word)
                count = count + 1
        except IOError as err:
            print 'File Error: ' + str(err) 
    distinct_words  = list(distinct_words)
    print "Total number of words are " + str(len(distinct_words))
    print "Total number of files are " + str(len(file_list))
    index_map_inverted = dict (zip(index_map.values(),index_map.keys()))
    print index_map
    print index_map_inverted
    index = [[0 for x in range(len(distinct_words))] for y in range(len(file_list))]
    #print index
    #print distinct_words
    for each in file_list:
        try:
            with open(each, 'r') as current_file:
                for current_line in current_file:
                    current_line = correct_sentence(removePunctuation(current_line.lower())).split(' ')
                    for each_word in current_line:
                        if each_word == '':
                            continue
                        elif stemming == True:
                            index[index_map[each]][distinct_words.index(stem(each_word))]+=1
                        else:
                            index[index_map[each]][distinct_words.index(each_word)]+=1
        except IOError as err:
            print 'File Error: ' + str(err) 
    #print index
    buildInvertedIndex()
    #buildNGramIndex(file_list, n)
#print ngrams_sentence("hello hello how are you  I am fine", 2)
readFiles(['a.txt', 'b.txt'], stemming = True, n =2)