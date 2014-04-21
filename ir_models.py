from build_index import *
query_distinct_words = []
query_frequency_matrix = []
    

def ngrams_query(n_input, n = 2):
    result = {}
    orig = n_input
    test = []
    n_input = '%' + n_input + '%' 
    # % used as start/end symbol here
    for each in n_input:
        test.append(each)
    n_input = test
    for i in range(len(n_input)-n+1):
        g = ''.join(n_input[i:i+n])
        if g in result:
            result[g].append(orig)
        else:
            result[g] =[orig]
    return set(result.keys())

def evaluate(eval_stack, result):
    eval_stack.reverse()
    first_operand = ''
    second_operand = ''
    n_operator = ''
    eval_copy = []
    prev_result = []
    for item in eval_stack:
        eval_copy.append(item)
    if len(eval_stack) < 2:
        return [],{}
    elif len(eval_stack) == 2:
        try:
            prev_result = boolean_inverted_index[(distinct_words.index(eval_stack[0]))]
            for i in range(len(prev_result)):
                item = prev_result[i]
                if item > 0:
                    result.add(i)
            return [], result
        except Exception:
            return [], [] 
    for each in eval_stack:
        eval_copy.remove(each)
        if each == '(':
            break
            #return eval_copy.reverse(), result
        elif each == '&&' and first_operand != '':
            n_operator = each
        elif each == '||' and first_operand == '':
            #print "############################################################"
            #print "Parse Error"
            return [], {}
        elif each == '||' and first_operand != '':
            n_operator = each
        elif each == '||' and first_operand == '':
            #print "############################################################"
            #print "Parse Error"
            return [], {}
        elif first_operand == '':
            first_operand = each
        elif (n_operator != '') or (first_operand != '' and n_operator == ''):
            second_operand = each
            if n_operator == '':
                n_operator = '&&'
            first_list = [0 for x in range(len(index_map))]
            if first_operand == 'result':
                first_list = prev_result
            second_list = [0 for x in range(len(index_map))]
            if first_operand in distinct_words:
                first_list = boolean_inverted_index[(distinct_words.index(first_operand))]
            if second_operand in distinct_words:
                second_list = boolean_inverted_index[(distinct_words.index(second_operand))] 
            temp =[]
            if n_operator == '||':
                temp = [k | l for k, l in zip(first_list, second_list)]
            else:
                temp = [k & l for k, l in zip(first_list, second_list)] 
            
            '''
            print "current_operation: ", first_operand, second_operand, n_operator
            print "current_status: ", first_list
            print "current_status: ", second_list
            print "Current_result: ", temp
            print temp
            '''
            second_operand, n_operator = '', ''
            first_operand = 'result'
            prev_result = temp
    #print "Now Showing", prev_result
    for i in range(len(prev_result)):
        item = prev_result[i]
        if item > 0:
            result.add(i)
    return eval_copy.reverse(), result
def validate_wildcard(sample, validator):
    new_sample = []
    for each in sample:
        flag = True
        for each_word in validator:
            if each_word not in each:
                flag = False
                break
        if flag == True:
            new_sample.append(each)
    return new_sample 

def boolean_model(parsed_query, special = 'NONE', n =2 ):
    #print distinct_words
    prev_result = []
    result = set()
    parsed_query.reverse()
    if special == 'NGRAM':
        print "####################################################"
        print "Ngram Boolean Model"
        print "####################################################"
        n_gram_words = []
        test = []
        for each in parsed_query:
            if '*' in each:
                continue
            else:
                test.append(each)
        test.insert(0, '(')
        #print test
        any_list, result = evaluate(test, result)
        #print "Intermnediate result\n", result
        test.remove('(')
        #print type(result)
        old_result = set()
        new_result= set()
        for each in parsed_query:
            if '*' in each:
                new_result = set()
                validation = each.split('*')
                t = each.replace('*', '')
                n_gram_words = ngrams_query(t.strip())
                n_gram_words.remove(t[-1] + '%')
                #print "ngram words are :"
                #print n_gram_words
                cur = set()
                for each in n_gram_words:
                    #print each
                    if each in n_gram_index:
                        #print n_gram_index[each]
                        if len(cur) < 1:
                            cur = set(n_gram_index[each])
                        else:
                            cur = cur.intersection(n_gram_index[each])
                        #print cur
                    else:
                        cur = cur.intersection(set())
                cur = validate_wildcard(cur, validation)
                #print "Current set after validation ", cur
                if (len(result) > 0) or len(test) > 0:
                    new_res = []
                    for i in range(len(index_map)):
                        if i in result:
                            new_res.append(1)
                        else:
                            new_res.append(0)
                    prev_result = new_res
                    #print prev_result
                else:
                    result = set()
                    prev_result = [1 for x in range(len(index_map))]
                #print "prev result ", prev_result
                for item in cur:
                    first_operand = 'result'
                    first_list = prev_result
                    second_operand = item
                    second_list = boolean_inverted_index[(distinct_words.index(stem(correct(second_operand))))]
                    temp =[]
                    temp = [k & l for k, l in zip(first_list, second_list)]
                    '''
                    print "current_status: ", first_list
                    print "current_status: ", second_list
                    print "Current_result: ", temp
                    print temp
                    '''
                    for i in range(len(temp)):
                        item = temp[i]
                        if item > 0:
                            new_result.add(i)
                #print "Old result: ", old_result 
                #print "new_result", new_result
                if len(old_result) < 1:
                    old_result = new_result
                else:
                    old_result = old_result.intersection(new_result)
            
        #print "Final calls ", result
        #print "Final out from there :", old_result
        #print len(test), test
        if len(test) < 1:
            result = old_result 
        #Uncomment this for more accurate result
        elif len(old_result) > 0: 
            result&=old_result # result|=old_result
        #print "Final result is", result
    else:
        print "####################################################"
        print "Simple Boolean Model"
        print "####################################################"
        parsed_query.insert(0, '(')
        parsed_query.append(')')
        #print parsed_query
        eval_stack = []
        for each in parsed_query:
            if each == ')':
                eval_stack, result = evaluate(eval_stack, result)
            else:
                eval_stack.append(each)
    #print result
    for item in result:
        print "Document: ", (index_map_inverted[item])
#print ngrams_query("hell")


def ranked_retrieval(parsed_query, vector = 'NONE'):
    global query_distinct_words, query_frequency_matrix
    doc_scores = [[x,0] for x in range(len(index_map_inverted))]
    sim_scores = [[x,0] for x in range(len(index_map_inverted))]
    if vector != 'NONE':
        print "####################################################"
        print "Vector Space Model"
        print "####################################################"
        #print parsed_query, type(parsed_query)
        query_magnitude = 0.0
        query_distinct_words = list(set(parsed_query))
        query_frequency_matrix = [0 for x in range(len(query_distinct_words))]
        for item in parsed_query:
            ind = query_distinct_words.index(item)
            query_frequency_matrix[ind]+=1
        for item in query_frequency_matrix:
            query_magnitude += (item * item)
        query_magnitude = math.sqrt(query_magnitude)
        query_frequency_matrix = [1 + math.log(x) for x in query_frequency_matrix]
        #print query_distinct_words
        #print query_frequency_matrix
        for i in range(len(tf_idf_score)):
            document_magnitude = 0.0
            for item in tf_idf_score[i]:
                document_magnitude+=(item*item)
            for each in parsed_query:
                try:
                    ind_1 = distinct_words.index(each)
                    ind_2 = query_distinct_words.index(each)
                    sim_scores[i][1]+=((tf_idf_score[i][ind_1] * query_frequency_matrix[ind_2])/(query_magnitude * document_magnitude))
                except Exception:
                    pass
        sim_scores.sort( key=itemgetter(1), reverse=True)
        for item in sim_scores[:10]:
            print "Document Name: " + index_map_inverted[item[0]] + " Relevance Score: " + str(item[1])
    else:
        print "####################################################"
        print "Ranked Retrieval Model"
        print "####################################################"
        for i in range(len(tf_idf_score)):
            for each in parsed_query:
                try:
                    ind = distinct_words.index(each)
                    doc_scores[i][1]+=tf_idf_score[i][ind]
                except Exception:
                    pass
        doc_scores.sort(reverse=True,key = itemgetter(1))
        for item in doc_scores[:10]:
            print "Document Name: " + index_map_inverted[item[0]] + " Relevance Score: " + str(item[1])