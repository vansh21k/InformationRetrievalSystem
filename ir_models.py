from build_index import *

def evaluate(eval_stack, result):
    eval_stack.reverse()
    first_operand = ''
    second_operand = ''
    n_operator = ''
    eval_copy = []
    prev_result = []
    for item in eval_stack:
        eval_copy.append(item)
    for each in eval_stack:
        eval_copy.remove(each)
        if each == '(':
            break
            #return eval_copy.reverse(), result
        elif each == 'and' and first_operand != '':
            n_operator = each
        elif each == 'and' and first_operand == '':
            print "############################################################"
            print "Parse Error"
            return [], {}
        elif each == 'or' and first_operand != '':
            n_operator = each
        elif each == 'or' and first_operand == '':
            print "############################################################"
            print "Parse Error"
            return [], {}
        elif first_operand == '':
            first_operand = each
        elif (n_operator != '') or (first_operand != '' and n_operator == ''):
            second_operand = each
            if n_operator == '':
                n_operator = 'and'
            first_list = [0 for x in range(len(index_map))]
            if first_operand == 'result':
                first_list = prev_result
            second_list = [0 for x in range(len(index_map))]
            if first_operand in distinct_words:
                first_list = boolean_inverted_index[(distinct_words.index(first_operand))]
            if second_operand in distinct_words:
                second_list = boolean_inverted_index[(distinct_words.index(second_operand))] 
            temp =[]
            if n_operator == 'or':
                temp = [k | l for k, l in zip(first_list, second_list)]
            else:
                temp = [k & l for k, l in zip(first_list, second_list)] 
            
            print "current_operation: ", first_operand, second_operand, n_operator
            print "current_status: ", first_list
            print "current_status: ", second_list
            print "Current_result: ", temp
            print temp
            second_operand, n_operator = '', ''
            first_operand = 'result'
            prev_result = temp
    print "Now Showing", prev_result
    for i in range(len(prev_result)):
        item = temp[i]
        if item > 0:
            result.add(i)
    return eval_copy.reverse(), result

def boolean_model(parsed_query, special = 'none' ):
    result = set()
    parsed_query.reverse()
    if special!='none':
        pass
    else:
        parsed_query.insert(0, '(')
        parsed_query.append(')')
        print parsed_query
        eval_stack = []
        for each in parsed_query:
            #print eval_stack
            if each == ')':
                eval_stack, result = evaluate(eval_stack, result)
            else:
                eval_stack.append(each)
    res = []
    print result
    for item in result:
        res.append(index_map_inverted[item])
    print "Result is: ", res
        