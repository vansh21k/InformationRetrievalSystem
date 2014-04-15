from preprocess import *
from ir_models import *
def get_query(sentence, model = "boolean", special = 'none'):
    if model == 'boolean' and special == 'none':
        boolean_model(correct_sentence(removePunctuation(sentence.lower())).strip().split())
    
get_query("Hello yes  no")