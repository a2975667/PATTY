import re
import networkx as nx
import matplotlib
import numpy as np
import spacy
import itertools as it
import os
nlp = spacy.load('en_core_web_sm')
from collections import defaultdict
import random
import copy
import sys
from utils import *
import pickle
import math
import scipy.stats as st
from entity import ENTITY_TYPES as ets

#pats, poscloud, suppcloud
def registersupport(syncloudwithsupport, syncloud, activesyn, syn, supp):
    setsup = set(supp.keys())

    if syn not in activesyn:
        activesyn[syn] = True
        syncloud[syn] = list()
        syncloud[syn].append(copy.deepcopy(setsup))
        syncloudwithsupport[syn] = dict()
        for k in supp:
            syncloudwithsupport[syn][k] = supp[k]
        return

    if activesyn[syn] == False:
        return

    if syn.startswith("<ENTITY>") == False:
        for sets in syncloud[syn]:
            if len(sets.intersection(setsup)) == 0:
                activesyn[syn] = False
            return

    syncloud[syn].append(copy.deepcopy(setsup))
    for k in supp:
        if k not in syncloudwithsupport[syn]:
            syncloudwithsupport[syn][k] = supp[k]
        else:
            syncloudwithsupport[syn][k] += supp[k]
    return

#pattern is a list- each list elements will be one of entity, n-grams, *
#sup is set of tuples. tuples size will be equal to no. of entity in pattern
def gensyngen(pats, poscloud, supps):
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
    for p in range(len(pats)):

        patstr = pats[p]
        pat = patstr.split(" ")
        poss = poscloud[patstr]
        poss = poss.split(" ")
        f = 0
        for i in range(len(poss)):
            if poss[i]=="<ENTITY>":
                pass
            elif poss[i] =="*":
                pass
            else:
                f = 1
                break
        if f==0:
            #ghanta+=1
            continue
        #typeuntye
        registersupport(syncloudwithsupport, syncloud, activesyn, patstr, supps[patstr])
        syn = copy.deepcopy(patstr)
        for entity in ets:
            print(syn)
            syn = syn.replace("<"+entity+">", "<ENTITY>")
            print(syn)
        # syn = syn.replace("<TARGET>", "<ENTITY>")
        #syn = syn.replace("<GENE>", "<ENTITY>")
        registersupport(syncloudwithsupport, syncloud, activesyn, syn, supps[patstr])

        #ngram contraction
        Nngram = list()
        for i in range(len(pat)):
            for entity in ets:
                if pat[i]== ("<"+entity+">") or pat[i] == "*":
                    pass
                else:
                    Nngram.append(i)
        try:
            assert len(Nngram)%3 == 0
        except AssertionError:
            print(patstr)

        for ii in range(0,len(Nngram),3):
            ing = Nngram[ii]
            syn = " "
            tok = []
            for i in range(len(pat)):
                if (i == ing+1) or (i== ing + 2):
                    pass
                elif i == ing:
                    if pat[i+3] != "*"  or pat[i-1] != "*":
                        tok.append("*")
                else:
                    tok.append(pat[i])
            syn = ' '.join(tok)
            syn = syn.replace(" * * "," * ")
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, supps[patstr])
            for entity in ets:
                syn = syn.replace("<"+entity+">", "<ENTITY>")
            #syn = syn.replace("<GENE>", "<ENTITY>")
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, supps[patstr])

        lenpos = 0

        for ipos in range(len(pat)):
            if (poss[ipos] == "<ENTITY>") or (poss[ipos] =="*"):
                continue
            else:
                lenpos += 1
                ptemp = copy.deepcopy(pat)

                ptemp[ipos] = poss[ipos]
                syn = ' '.join(ptemp)
                registersupport(syncloudwithsupport, syncloud, activesyn, syn, supps[patstr])

                ptemp[ipos] = "[WORD]"
                syn = ' '.join(ptemp)
                registersupport(syncloudwithsupport, syncloud, activesyn, syn, supps[patstr])

                ptemp[ipos] = poss[ipos]
                for entity in ets:
                    syn = syn.replace("<"+entity+">", "<ENTITY>")
                #syn = syn.replace("<GENE>", "<ENTITY>")
                registersupport(syncloudwithsupport, syncloud, activesyn, syn, supps[patstr])

                ptemp[ipos] = "[WORD]"
                syn = ' '.join(ptemp)
                for entity in ets:
                    syn = syn.replace("<"+entity+">", "<ENTITY>")
                #syn = syn.replace("<GENE>", "<ENTITY>")
                registersupport(syncloudwithsupport, syncloud, activesyn, syn, supps[patstr])



        if lenpos > 1:
            ptemp = copy.deepcopy(pat)
            for ipos in range(len(pat)):
                if (poss[ipos] == "<ENTITY>") or (poss[ipos] =="*"):
                    pass
                else:
                    ptemp[ipos] = poss[ipos]
            syn = ' '.join(ptemp)
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, supps[patstr])
            ptemp = copy.deepcopy(pat)
            for ipos in range(len(pat)):
                if (poss[ipos] == "<ENTITY>") or (poss[ipos] =="*"):
                    pass
                else:
                    ptemp[ipos] = "[WORD]"
            syn = ' '.join(ptemp)
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, supps[patstr])

        if lenpos > 1:
            ptemp = copy.deepcopy(poss)
            for ipos in range(len(pat)):
                if (poss[ipos] == "<ENTITY>") or (poss[ipos] =="*"):
                    pass
                else:
                    ptemp[ipos] = poss[ipos]
            syn = ' '.join(ptemp)
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, supps[patstr])
            ptemp = copy.deepcopy(poss)
            for ipos in range(len(pat)):
                if (poss[ipos] == "<ENTITY>") or (poss[ipos] =="*"):
                    pass
                else:
                    ptemp[ipos] = "[WORD]"
            syn = ' '.join(ptemp)
            registersupport(syncloudwithsupport, syncloud, activesyn, syn, supps[patstr])

        #raise ValueError("bs")


    retsyncloud = dict()
    untypedcloud = dict()
    for syn in syncloud:
        if activesyn[syn] == True:
            if syn.startswith("<ENTITY>") == False:
                retsyncloud[syn] = copy.deepcopy(syncloudwithsupport[syn])
            else:
                untypedcloud[syn] = copy.deepcopy(syncloudwithsupport[syn])
    #print(ghanta)
    return retsyncloud, untypedcloud
