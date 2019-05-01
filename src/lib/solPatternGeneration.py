# import re
# import networkx as nx
# import matplotlib
# import numpy as np
# import spacy
# import itertools as it
# import os
# nlp = spacy.load('en_core_web_sm')
# from collections import defaultdict
# import random
# import copy
# import sys
# from utils import *
# import pickle
# import math
# import scipy.stats as st
# from entity_extractor import load_entity
# ets = load_entity()
#from entity import ENTITY_TYPES as ets
from sentence.sentence import Pattern

#replacing non entity non frequent n gram by wildcard


def generate_sol_patterns(corpus):
    """A method to generate SOL patterns given the textual patterns and ngrams.
    Parameters
    ----------
    patterns : type List
        Textual Patterns
    ngrams : type List of tuples
        NGrams
    Returns
    -------
    type List
        Returns SOL Patterns
    """

    pos_patterns = []

    idx = 0
    for pattern in corpus.all_textual_pattern:
        words = pattern.pattern.split(" ")
        line = []
        pos_line = []
        pos = []
        for word in words:
            if word.startswith(tuple([entity+'_' for entity in corpus.entity])):
                line.append("<ENTITY>")
                #pos_line.append("<ENTITY>")
            else:
                line.append(word)
                #pos_line.append(post[pattern_index][word_index])
        line = ' '.join(line)
        times = 0
        ref_ngram = []
        for ngram_pattern in corpus.ngram:
            if ngram_pattern.pattern in line:
                ref_ngram.append(ngram_pattern.pid)
                if times <= 4:
                    line = line.replace(
                        " "+ngram_pattern.pattern+" ", " $ $ $ ")
                    times += 1
                else:
                    break
        words = line.split(" ")
        assert len(words) == len(pattern.pattern.split(" "))
        for i, _ in enumerate(words):
            if words[i] != "$" and words[i] != "<ENTITY>":
                words[i] = "*"
        toks = pattern.pattern.split(" ")
        for i, _ in enumerate(words):
            if words[i] == "<ENTITY>":
                pos_line.append(toks[i])
                pos.append("<ENTITY>")
            elif words[i] == "$":
                pos_line.append(toks[i])
                pos.append(pattern.pos[i])
            elif words[i] != words[i-1]:
                pos_line.append("*")
                pos.append("*")
        strpos = ' '.join(pos_line)
        pos = ' '.join(pos)

        p = Pattern(strpos, idx)
        p.ref_ngram = ref_ngram
        p.ref_pattern = pattern.pid
        p.pos = pos
        p.sentence_id = pattern.sentence_id

        pos_patterns.append(p)
        idx += 1
    corpus.pos_patterns = pos_patterns

#replacing non entity non frequent n gram by wildcard
def generate_sol_pos_patterns(corpus):
    #patterns, ngrams, post
    """A method to generate SOL Patterns with POS tags.
    
    Parameters
    ----------
    patterns : type List
        Textual Patterns
    ngrams : type List of tuples
        NGrams
    post : type List
        POS Tag patterns
    Returns
    -------
    type List
        List of patterns with POS Tags
    """
    sol_pos_patterns = []
    idx = 0
    for pattern in corpus.all_textual_pattern:
        
        words = pattern.pattern.split(" ")
        line = []
        pos_line = []
        for word in words:
            if word.startswith(tuple([entity+'_' for entity in corpus.entity])):
                line.append("<ENTITY>")
                #pos_line.append("<ENTITY>")
            else:
                line.append(word)
                #pos_line.append(post[pattern_index][word_index])
        line = ' '.join(line)
        times = 0
        ref_ngram = []
        for ngram_pattern in corpus.ngram:
            if ngram_pattern.pattern in line:
                ref_ngram.append(ngram_pattern.pid)
                if times <= 4:
                    line = line.replace(" "+ ngram_pattern.pattern + " ", " $ $ $ ")
                    times += 1
                else:
                    break
        words = line.split(" ")
        for i, _ in enumerate(words):
            if words[i] != "$" and words[i] != "<ENTITY>" :
                words[i] = "*"
        for i, _ in enumerate(words):
            if words[i] == "<ENTITY>":
                pos_line.append("<ENTITY>")
            elif words[i] == "$":
                pos_line.append(pattern.pos[i])
            elif words[i] != words[i-1]:
                pos_line.append("*")
        strpos =  ' '.join(pos_line)

        p = Pattern(strpos, idx)
        p.ref_ngram = ref_ngram
        p.ref_pattern = pattern.pid
        p.sentence_id = pattern.sentence_id

        sol_pos_patterns.append(p)
        idx += 1

    corpus.sol_pos_patterns = sol_pos_patterns


def obtainpat(patlist, ets):
    strpat = list()
    entlist = list()
    toks = patlist.split(" ")
    cnt = 0
    for w in toks:
        flg = False
        for entity in ets:
            if flg:
                break
            if w.startswith(entity):
                string = '<'+str(entity)+'>'
                strpat.append(string)
                entlist.append(w)
                flg = True
        if not flg:
            strpat.append(w)
            if w!="*":
                cnt+=1

    try:
        assert cnt%3==0
    except AssertionError:
        pass
    strpat = ' '.join(strpat)
    entstr = ' '.join(entlist)
    return strpat, entstr

def get_support_of_sols(corpus):
    from pprint import pprint; pprint(vars(corpus.pos_patterns[0]))
    
    #sol_pos_patterns = [p.pattern for p in corpus.sol_pos_patterns]
    """A function to get support of each of the SOL and POS replaced SOL patterns.

    Parameters
    ----------
    sol_patterns : LIST
    sol_pos_patterns : LIST

    Returns
    -------
    type Tuple
        Returns tuple of dictionaries with keys as pattern and value as support.

    """

    suppcloud = dict()
    pats = list()
    counter = 0

    for idx, sol_pattern in enumerate(corpus.pos_patterns):
        pat, ent = obtainpat(sol_pattern.pattern, corpus.entity)

        if pat not in suppcloud:

            p = Pattern(pat, idx)
            pats.append(pat)
            suppcloud[pat] = p
            p.pos = [sol_pattern.pos]
            p.sentence_id = sol_pattern.sentence_id

            counter += 1
        
        if ent not in suppcloud[pat].entity_list:
            suppcloud[pat].entity_list[ent] = 1
            suppcloud[pat].sentence_id += sol_pattern.sentence_id
        else:
            suppcloud[pat].entity_list[ent] += 1
            suppcloud[pat].sentence_id += sol_pattern.sentence_id

    corpus.pats = pats
    corpus.suppcloud = suppcloud

    # print(pats)
    # print(poscloud)
    # print(suppcloud)
    # return pats, poscloud, suppcloud
