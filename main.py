from preprocess import *
from ir_models import *
import simpleguitk as simplegui

##STATE VARIABLES
MODEL = "BOOLEAN" #"RANKER"
SPECIAL = "NONE" #"VECTOR" "NGRAM"

def re_build_index(): 
    os.chdir('../')
    files = get_files()
    readFiles(files, True, NGRAM_PARAMETER)

def get_query(sentence, model = "BOOLEAN", special = 'NONE', n = 2):
    print "Search Results for: %s " % sentence
    if model == 'BOOLEAN' and special == 'NONE':
        temp = []
        for each in ((removePunctuation(sentence.lower())).strip().split()): 
            if each in ['&&', '||'] or '*' in each:
                temp.append(each)
            else:
                temp.append(stem(correct(each)))
        boolean_model(temp, special, n)
    elif model == 'BOOLEAN' and special == 'NGRAM':
        temp = []
        for each in ((removePunctuation(sentence.lower())).strip().split()): 
            if each in ['&&', '||'] or '*' in each:
                temp.append(each)
            else:
                temp.append(stem(correct(each)))
        boolean_model(temp, special, n)
    elif model == 'RANKER':
        temp = []
        for each in ((removePunctuation(sentence.lower())).strip().split()): 
            if each in ['&&', '||'] or '*' in each:
                temp.append(each)
            else:
                temp.append(stem(correct(each)))
        ranked_retrieval(temp, special)

def draw(canvas):
    canvas.draw_text("Welcome!", [150, 50], 20, "Green")
    canvas.draw_text("MODEL: " + str(MODEL), [20, 400], 10, "Red")
    canvas.draw_text("SPEC: " + str(SPECIAL), [20, 450], 10, "Red")
    canvas.draw_text("NGRAM Value: " + str(NGRAM_PARAMETER), [300, 400], 10, "Red")
    
def get_input(inp):
    print 
    print "####################################################"
    get_query(inp.strip(), MODEL, SPECIAL, NGRAM_PARAMETER)
    print "####################################################"
    print
def boolean_mode():
    global MODEL, SPECIAL
    MODEL = "BOOLEAN"
    SPECIAL = "NONE"
def n_gram_boolean():
    global MODEL, SPECIAL
    MODEL =  "BOOLEAN"
    SPECIAL = "NGRAM"
def ranker_mode():
    global MODEL, SPECIAL
    MODEL = "RANKER"
    SPECIAL = "NONE"
def vector_mode():
    global MODEL, SPECIAL
    MODEL  = "RANKER"
    SPECIAL = "VECTOR"
def get_n(inp):
    global NGRAM_PARAMETER
    try:
        NGRAM_PARAMETER = int(inp)
    except Exception:
        NGRAM_PARAMETER = 2
     

frame = simplegui.create_frame("V_SEARCH", 400, 500)
frame.set_draw_handler(draw)
search_box = frame.add_input("Enter Search Query ", get_input,100)
re_build = frame.add_button("REBUILD_INDEX", re_build_index)
display_button = frame.add_button("DISPLAY", display_all)
boolean_button = frame.add_button("BOOLEAN_MODE", boolean_mode)
ngram_button = frame.add_button("N-Gram Boolean Model", n_gram_boolean)
ranker_button = frame.add_button("Ranked Retrieval Model", ranker_mode)
vector_button = frame.add_button("Vector Space Model", vector_mode)
n_gram_box = frame.add_input("N gram number", get_n, 20)
frame.start()
'''
while True:
    query = raw_input("Enter Search Query (Type *** to quit)\n")
    if query == "***":
        break
    get_query(query, special = 'vector', model='ranker')
    print
    print '######################################################'
    print
'''