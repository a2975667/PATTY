""" extract all entities in the document """

import sys
import re
from collections import defaultdict
import pickle


def extract_entity(filename):
    '''given file, extract possible entities'''

    entity_set = defaultdict(lambda:1)
    pattern = re.compile(r'^[A-Z]+$')

    f = open(filename, 'r')
    for line in f:
        tokens = line.split(' ')
        for token in tokens:
            if '_' in token:

                entity_type = token.split('_')[0]

                if re.search(pattern, entity_type):
                    entity_set[entity_type] += 1

    return define_entity_set(entity_set)

def define_entity_set(entity_set):
    '''return final entity set'''
    total_count = sum(entity_set.values())
    final_set = []
    for key in entity_set:
        if (entity_set[key]/total_count)*100 > 0.01:
            final_set.append(key)
    
    return final_set

def dump_entity(filename):
    ''' dump entity list to pikle data '''
    entity_set = extract_entity(filename)
    print ("located", len(entity_set), "entites")
    with open('entity.data', 'wb') as filehandle:
        pickle.dump(entity_set, filehandle)

def load_entity():
    with open('entity.data', 'rb') as filehandle:  
    # read the data as binary data stream
        return pickle.load(filehandle)

