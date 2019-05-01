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
import copy
# import sys
# from utils import *
# import pickle
# import math
# import scipy.stats as st
# #from entity import ENTITY_TYPES as ets
# from entity_extractor import load_entity
# ets = load_entity()
import sys
from pprint import pprint
from sentence.sentence import Pattern

#pats, poscloud, suppcloud
def registersupport(syncloudwithsupport, syncloud, activesyn, syn, supp):
    setsup = list(set(supp.entity_list.keys()))
    
    if syn not in syncloudwithsupport:
        p = Pattern(syn,len(syncloudwithsupport))
        p.status = True
        for k in supp.entity_list:
            p.entity_list[k] = supp.entity_list[k]
        p.sentence_id = list(set(supp.sentence_id))
        p.pos = supp.pos
        syncloudwithsupport[syn] = p
   
        return

    if syncloudwithsupport[syn].status == False:
        return


        # print("--------")
        # print(syncloudwithsupport)
        # print(syncloud)
        # print(activesyn)
        # print("--------")
        # pprint(vars(p))
        # sys.exit()

    if syn.startswith("<ENTITY>") == False:
        key_set = set([key for key in syncloudwithsupport[syn].entity_list])
        if len(key_set.intersection(setsup)) == 0:
            syncloudwithsupport[syn].status = False
            return #weird return position, reference to original code


    for k in supp.entity_list:
        if k in syncloudwithsupport[syn].entity_list:
            syncloudwithsupport[syn].entity_list[k] += supp.entity_list[k]
        else:
            syncloudwithsupport[syn].entity_list[k] = supp.entity_list[k]
    #syncloud[syn].append(copy.deepcopy(setsup))
    # print(syncloud)
    # for k in supp.entity_list:
    #     print(supp.entity_list[k])
    #     if k not in syncloudwithsupport[syn]:
    #         syncloudwithsupport[syn][k] = supp.entity_list[k]
    #     else:
    #         syncloudwithsupport[syn][k] += supp.entity_list[k]
    #sys.exit()
    return

#pattern is a list- each list elements will be one of entity, n-grams, *
#sup is set of tuples. tuples size will be equal to no. of entity in pattern
def gensyngen(corpus):
    #pats, poscloud, suppcloud
    """A function to do syntactic pattern generalization.
    Parameters
    ----------
    pats : List of patterns.
    poscloud : POS support of patterns
    """

    syncloud = dict()
    activesyn = dict()
    syncloudwithsupport = dict()
    #ghanta = 0
    for idx, pattern in enumerate(corpus.pats):
        pat = pattern.split(" ")
        poss = corpus.suppcloud[pattern].pos[0].split(" ")
        
        f = 0
        
        for pp in poss:
            if pp == "<ENTITY>":
                pass
            elif pp == "*":
                pass
            else:
                f = 1
                break
        if f==0:
            #ghanta+=1
            continue
        #typeuntye

        registersupport(syncloudwithsupport, syncloud, activesyn, pattern, corpus.suppcloud[pattern])
        syn = copy.deepcopy(pattern)
        for entity in corpus.entity:
            entity_string='<'+str(entity)+'>'
            syn = syn.replace(entity_string, "<ENTITY>")
        registersupport(syncloudwithsupport, syncloud, activesyn, syn, corpus.suppcloud[pattern])

        #ngram contraction
        Nngram = list()
        entity_types = ['<'+ str(entity)+'>' for entity in corpus.entity]
        for i in range(len(pat)):
            if pat[i] in entity_types or pat[i] == "*":
                pass
            else:
                Nngram.append(i)
        try:
            assert len(Nngram)%3 == 0
        except AssertionError:
            print(pattern)

        for ii in range(0,len(Nngram),3):
            ing = Nngram[ii]
            syn = " "
            tok = []
            for i in range(len(pat)):
                if (i == ing+1) or (i== ing + 2):
                    pass
                elif i == ing:
                    if len(pat) > i+3:
                        if pat[i+3] != "*"  or pat[i-1] != "*":
                            tok.append("*")
                else:
                    tok.append(pat[i])
            syn = ' '.join(tok)
            syn = syn.replace(" * * "," * ")
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, corpus.suppcloud[pattern])
            for entity in corpus.entity:
                entity_string='<'+str(entity)+'>'
                syn = syn.replace(entity_string, "<ENTITY>")
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, corpus.suppcloud[pattern])

        lenpos = 0

        for ipos in range(len(pat)):
            if (poss[ipos] == "<ENTITY>") or (poss[ipos] =="*"):
                continue
            else:
                lenpos += 1
                ptemp = copy.deepcopy(pat)

                ptemp[ipos] = poss[ipos]
                syn = ' '.join(ptemp)
                registersupport(syncloudwithsupport, syncloud, activesyn, syn, corpus.suppcloud[pattern])

                ptemp[ipos] = "[WORD]"
                syn = ' '.join(ptemp)
                registersupport(syncloudwithsupport, syncloud, activesyn, syn, corpus.suppcloud[pattern])

                ptemp[ipos] = poss[ipos]
                syn = ' '.join(ptemp)
                for entity in corpus.entity:
                    entity_string='<'+str(entity)+'>'
                    syn = syn.replace(entity_string, "<ENTITY>")
                registersupport(syncloudwithsupport, syncloud, activesyn, syn, corpus.suppcloud[pattern])

                ptemp[ipos] = "[WORD]"
                syn = ' '.join(ptemp)
                for entity in corpus.entity:
                    entity_string='<'+str(entity)+'>'
                    syn = syn.replace(entity_string, "<ENTITY>")
                registersupport(syncloudwithsupport, syncloud, activesyn, syn, corpus.suppcloud[pattern])



        if lenpos > 1:
            ptemp = copy.deepcopy(pat)
            for ipos in range(len(pat)):
                if (poss[ipos] == "<ENTITY>") or (poss[ipos] =="*"):
                    pass
                else:
                    ptemp[ipos] = poss[ipos]
            syn = ' '.join(ptemp)
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, corpus.suppcloud[pattern])
            ptemp = copy.deepcopy(pat)
            for ipos in range(len(pat)):
                if (poss[ipos] == "<ENTITY>") or (poss[ipos] =="*"):
                    pass
                else:
                    ptemp[ipos] = "[WORD]"
            syn = ' '.join(ptemp)
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, corpus.suppcloud[pattern])

        if lenpos > 1:
            ptemp = copy.deepcopy(poss)
            for ipos in range(len(pat)):
                if (poss[ipos] == "<ENTITY>") or (poss[ipos] =="*"):
                    pass
                else:
                    ptemp[ipos] = poss[ipos]
            syn = ' '.join(ptemp)
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, corpus.suppcloud[pattern])
            ptemp = copy.deepcopy(poss)
            for ipos in range(len(pat)):
                if (poss[ipos] == "<ENTITY>") or (poss[ipos] =="*"):
                    pass
                else:
                    ptemp[ipos] = "[WORD]"
            syn = ' '.join(ptemp)
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, corpus.suppcloud[pattern])

    retsyncloud = dict()
    untypedcloud = dict()
    for syn in syncloudwithsupport:
        if syncloudwithsupport[syn].status == True:
            if syn.startswith("<ENTITY>") == False:
                retsyncloud[syn] = copy.deepcopy(syncloudwithsupport[syn])
            else:
                untypedcloud[syn] = copy.deepcopy(syncloudwithsupport[syn])
    #print(ghanta)
    [pprint(vars(retsyncloud[x])) for x in retsyncloud]
    [pprint(vars(untypedcloud[x])) for x in untypedcloud]
    
    return retsyncloud, untypedcloud