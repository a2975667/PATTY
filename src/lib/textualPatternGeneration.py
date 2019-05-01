# import re
# import networkx as nx
# import matplotlib
# import numpy as np
from lib.helper import check_entities, adv_mod_deps
from lib.helper import shortest_dependency_path as sdp
import sys
import spacy
import itertools as it
from sentence.sentence import Pattern
# import os
nlp = spacy.load('en_core_web_sm')
# from collections import defaultdict
# import random
# import copy
# from utils import *
# import pickle
# import math
# import scipy.stats as st
# #from entity import ENTITY_TYPES as ets
# from entity_extractor import load_entity
# ets = load_entity()

def generate_textual_patterns(corpus):
    """A method to generate textual patterns given the corpus.

    Parameters
    ----------
    corpus : Corpus Object

    Returns
    -------
    type List
        List of textual patterns

    """
    #textual_patterns = []
    corpus.sentence_with_textual_pattern = []
    corpus.all_textual_pattern = []
    counter = 0
    for i, sentence in enumerate(corpus.corpus):
        sys.stderr.write('Processing...{0:.3%}\r'.format(i/corpus.count))
        
        dep_parse = nlp(sentence.sentence)
        entity_length, entities = check_entities(sentence.sentence, corpus.entity)

        try:
            if entity_length == 2:
                path = sdp(dep_parse, entities[0], entities[1])
                if len(path) != 2:
                    
                    # getting pattern
                    shortest_path = ' '.join(path)
                    pattern = adv_mod_deps(shortest_path, dep_parse)
                    pattern = to_lower_case(pattern, corpus.entity)
                    
                    # creating pattern object
                    p = Pattern(pattern, counter)
                    p.add_id(sentence.sid)
                    sentence.textual_patterns.append(p)
                    counter += 1
                    
                    # updating pattern and sentence object
                    sentence.textual_patterns.append(counter)
                    corpus.sentence_with_textual_pattern.append(sentence)
                    corpus.all_textual_pattern.append(p)

            elif entity_length > 2:
                pairs = it.combinations(entities, 2)
                for pair in pairs:
                    path = sdp(dep_parse, pair[0], pair[1])
                    if len(path) != 2:
                        shortest_path = ' '.join(path)
                        pattern = adv_mod_deps(shortest_path, dep_parse)
                        pattern = to_lower_case(pattern, corpus.entity)
                        # creating pattern object
                        p = Pattern(pattern, counter)
                        p.add_id(sentence.sid)
                        sentence.textual_patterns.append(counter)
                        counter += 1
                        
                        # updating pattern and sentence object
                        sentence.textual_patterns.append(p)
                        corpus.sentence_with_textual_pattern.append(sentence)
                        corpus.all_textual_pattern.append(p)

            if sentence.sentence.strip() == '':
                continue
            corpus.sentence_with_textual_pattern.append(sentence)

        except Exception as e:
            #print(e)
            pass
    
    print('\nWriting to file...')
    with open('textual_pattern.txt', "w") as f:
        for tp in corpus.all_textual_pattern:
            f.write(str(tp.pattern) + "\n")


def to_lower_case(pattern, ets):
    """Converts patterns to lower case barring the entities.
    Parameters
    ----------
    pattern_file : type Path
        The file containing the textual patterns
    Returns
    -------
    type List
        Returns the list of textual patterns converted to lowercase.
    """
    line = pattern.strip()
    # try:
    #     #line = str(line, 'utf-8')
    #     line = line.encode("utf-8")
    # except Exception as e:
    #     print(e)
    # print(line)
    w = line.split(" ")
    if(len(w) <=2):
        return line
    f = 0
    if w[0].startswith(tuple([e+'_' for e in ets])):
        pass
    else:
        f = 1
    if w[len(w)-1].startswith(tuple([e+'_' for e in ets])):
        pass
    else:
        f = 1
    if f == 0:
        fl = 0
        for ii in range(len(w)):
            i = w[ii]
            
            fl = sum([1* ((x+'_') in i) for x in ets])
            #fl = 1*("CHEMICAL_" in i) + 1*("DISEASE_" in i) + 1*("GENE_" in i)
            if fl!=1:
                w[ii]  = str.lower(i)
            if fl > 1:
                break
        if fl > 1:
            return line
        strmed = ' '.join(w[1:len(w)-1])
        strmed = str(w[0]) + " " + strmed + " " + str(w[len(w)-1])

    return strmed
