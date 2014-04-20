from preprocess import *
from ir_models import *

def get_query(sentence, model = "boolean", special = 'none', n = 2):
    if model == 'boolean' and special == 'none':
        temp = []
        for each in ((removePunctuation(sentence.lower())).strip().split()): 
            if each in ['&&', '||'] or '*' in each:
                temp.append(each)
            else:
                temp.append(stem(correct(each)))
        boolean_model(temp, special, n)
    elif model == 'boolean' and special == 'ngram':
        temp = []
        for each in ((removePunctuation(sentence.lower())).strip().split()): 
            if each in ['&&', '||'] or '*' in each:
                temp.append(each)
            else:
                temp.append(stem(correct(each)))
        boolean_model(temp, special, n)
    elif model == 'ranker':
        temp = []
        for each in ((removePunctuation(sentence.lower())).strip().split()): 
            if each in ['&&', '||'] or '*' in each:
                temp.append(each)
            else:
                temp.append(stem(correct(each)))
        ranked_retrieval(temp, special)


while True:
    query = raw_input("Enter Search Query (Type *** to quit)\n")
    if query == "***":
        break
    get_query(query, special = 'ngram', model='boolean')
    print
    print '######################################################'
    print