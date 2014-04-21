'''
Created on 10-Apr-2014

@author: VANSH
'''
import os
import math
from stemming.porter2 import stem
import string
from operator import itemgetter
import glob
from preprocess import *

NGRAM_PARAMETER = 2
tf_idf_score = []
document_frequency = [] #This is the idf matrix instead
collection_frequency = []
log_weighted_doc_term_matrix= []
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
    for each in correct_sentence(removePunctuation(n_input.lower())).strip().split():
        ngrams(each, n)
    
def ngrams(n_input, n = 2):
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
    #print n_gram_index
def buildInvertedIndex():
    ''' Generate the inverted index'''
    global index
    global distinct_words
    global index
    global index_map
    global inverted_index_list
    global boolean_inverted_index
    global log_weighted_doc_term_matrix
    global collection_frequency
    global document_frequency
    global tf_idf_score
    inverted_index_list = [[0 for x in range(len(index_map))] for y in range(len(distinct_words))]
    log_weighted_doc_term_matrix = [[0 for x in range(len(distinct_words))] for x in range(len(index_map))]
    tf_idf_score = [[0 for x in range(len(distinct_words))] for x in range(len(index_map))]
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
    #print inverted_index
    for i in range(len(distinct_words)):
        each = distinct_words[i]
        for each_row in inverted_index[each]:
            if each_row != []:
                inverted_index_list[i][index_map[each_row[0]]]+=each_row[1]
    #print "Now giving Inverted Index list"
    #print inverted_index_list
    for each in inverted_index_list:
        temp = []
        for each_list in each:
            if each_list > 0:
                temp.append(1)
            else:
                temp.append(0)
        boolean_inverted_index.append(temp)
    #print len(inverted_index_list)
    #print len(distinct_words)
    for i in range(len(index_map)):
        for j in range(len(inverted_index)):
            each = inverted_index_list[j]
            if each[i] == 0:
                log_weighted_doc_term_matrix[i][j] = 0
            else:
                log_weighted_doc_term_matrix[i][j] = 1 + math.log(each[i]) 
    #print "Log weighted Index terms are :"
    #print log_weighted_doc_term_matrix
    collection_frequency = [sum(x) for x in inverted_index_list]
    #print "Now computing idf matrix"
    document_frequency = [0 for x in range(len(distinct_words))]
    #print len(inverted_index_list)
    #print len(document_frequency)
    for i in range(len(inverted_index_list)):
        each = inverted_index_list[i]
        freq = 0
        for x in each:
            if x > 0:
                freq+=1
        document_frequency[i] = freq
        if freq > 0:
            document_frequency[i] = math.log((len(index_map))/ freq) 
    #print "Document Frequency is: "   
    #print document_frequency
    #print "finally the tf-idf matrix is:"
    for i in range(len(log_weighted_doc_term_matrix)):
        for j in range(len(document_frequency)): 
            tf_idf_score[i][j] = log_weighted_doc_term_matrix[i][j] * document_frequency[j] 
    #print tf_idf_score
    #print len(tf_idf_score)
    #print "The boolean inverted"
    #print boolean_inverted_index

def readFiles(file_list, stemming = False, n = 2):
    '''Read the files, apply normalization and make the files ready for indexing
       Current Standard of Normalization: lower case, remove punctuation, spell check
       To add: Stop Word List
     '''
    global tf_idf_score 
    global document_frequency 
    global collection_frequency 
    global log_weighted_doc_term_matrix
    global inverted_index_list
    global index_map 
    global index 
    global inverted_index
    global distinct_words 
    global n_gram_index 
    global boolean_inverted_index 
    global index_map_inverted   
    tf_idf_score = []
    document_frequency = [] #This is the idf matrix instead
    collection_frequency = []
    log_weighted_doc_term_matrix= []
    inverted_index_list = []
    index_map = {}
    index = {} #2d term Frequence Matrix
    inverted_index = {} #Inverted Index
    distinct_words = set() #Set to identify all words 
    n_gram_index = {} # Key: bigram, Value: List of terms 
    boolean_inverted_index = [] #Boolean index to support wild card queries and phrasal queries
    index_map_inverted = {}

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
    index_map_inverted = dict (zip(index_map.values(),index_map.keys()))
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
    buildNGramIndex(file_list, n)

def get_files():
    os.chdir("data/")
    return glob.glob('*.txt')

files = get_files()
readFiles(files, stemming = True, n = NGRAM_PARAMETER)
print index_map
print index_map_inverted
def display_all():
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    print "No. of files used for indexing are: ", len(files)
    print "Files used for indexing:"
    for each in files:
        print each
    print "#####################################################"
    print "No. of Distinct words found are: ", len(distinct_words)
    print "The words are: "
    for each in distinct_words:
        print each
    print "#################################################"
    print "Document frequency: "
    for i in range(len(distinct_words)):
        print distinct_words[i] + '\t' + str(document_frequency[i])
    print "#################################################"
    print "Collection frequency: "
    for i in range(len(distinct_words)):
        print distinct_words[i] + '\t' + str(collection_frequency[i])
    print "###################################################"
    print "Inverted Index as list:"
    for item in inverted_index:
        print item + '\t' + str(inverted_index[item])
    print '#####################################################'
    print "Inverted Index Matrix: "
    for i in range(len(inverted_index_list)):
        print distinct_words[i] + '\t' + str(inverted_index_list[i])
    print "#####################################################"
    print "N-Gram index for wildcard queries:"
    for item in n_gram_index:
        print item + '\t' + str(n_gram_index[item])
    print "#####################################################"
    print "Boolean inverted index matrix: "
    print index_map_inverted, len(index_map_inverted)
    print boolean_inverted_index, len(boolean_inverted_index)
    for i in (index_map_inverted):
        print index_map_inverted[i] + '\t' + str(boolean_inverted_index[i]) 
    print '########################################################'
    print "TF-IDF scores"
    for i in (index_map_inverted):
        print index_map_inverted[i] + '\t' +  str(tf_idf_score[i]) 
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
display_all()