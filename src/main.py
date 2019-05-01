import math
import pickle
import sys
import copy
import random
from collections import defaultdict
import os
from utils.preprocess import preprocess
from lib import textualPatternGeneration as tPG
from lib import ngramMining as ngMine
from lib import solPatternGeneration as sPG
from lib.helper import generate_pos_tags_for_patterns as gen_pos
from lib import syntacticPatternGeneralization as syntacticPG
from utils import post_processing as pp
from pprint import pprint

if __name__ == "__main__":
    print("Program Started...")
    params = {'data_dir': '/'.join(sys.argv[1].split('/')[:-1]), 'corpus_fn': sys.argv[1].split('/')[-1]}
    os.chdir(params['data_dir'])
    
    #Input Data pre. 
    corpus = preprocess(params)
    #corpus.print_info()
    

    print("Generating Textual Patterns")
    tPG.generate_textual_patterns(corpus)
    print("Done generating textual patterns.")
    
    print("Generating POS tags")
    gen_pos(corpus)
    print("Done generating POS tags.")
    

    print("Mining sequences")
    ngMine.generate_seqmining_dataset(corpus)
    ngMine.generate_frequent_ngrams(corpus, 2)
    print("Done Mining sequences.")

    
    print("Mining sequences")
    sPG.generate_sol_patterns(corpus)
    #sPG.generate_sol_pos_patterns(corpus)
    print("Done Mining sequences.")

    print("Calculating Support")
    sPG.get_support_of_sols(corpus)
    print("Done calculation.")

    print("Final Calculation")
    p_s_c, utc = syntacticPG.gensyngen(corpus)
    final = pp.get_strength_confidence(p_s_c, utc, corpus)
    
    with open('final.txt', 'w') as f:
        for key in final:
            string = key + '\t'
            string += str(final[key]['confidence']) + '\t'
            string += str(final[key]['data'].sentence_id)
            f.write(string+ '\n')
    
    # #lconfpat = sorted(conf_pat.items(), key=lambda x: (strength_pat[x[0]]), reverse = True)
    # #pprint(final)
    
    
    # # print(strength_pat)
    # # print(conf_pat)
    
    # # 
    
    # # print("Complete")
    # sys.exit()
    # with open('pat_pos_supp.pkl', 'wb') as f:
    #     pickle.dump([pats, poscloud, suppcloud], f)

    # with open('strengthconf.pkl', 'wb') as f:
    #     pickle.dump([strength_pat, conf_pat], f)
    


    
    # from syntacticPatternGeneralization import *
    # from solPatternGeneration import *
    # from prefixTreeConstruction import *
    # from ngramMining import *
    # from mineSubsumptions import *
    # from dagConstruction import *
    # import utils

    # #post = generate_pos_tags_for_patterns(textual_patterns, "TexPatPosTag.pkl")
    # # with open('sp_spp.pkl', 'wb') as f:
    # #     pickle.dump([sol_patterns, sol_pos_patterns], f)


    # p_s_c, utc = gensyngen(pats, poscloud, suppcloud)
    # with open('pscaftersec5.pkl', 'wb') as f:
    #     pickle.dump([p_s_c, utc], f)

    # strength_pat, conf_pat = get_strength_confidence(p_s_c, utc, corpus)
    # with open('strengthconf.pkl', 'wb') as f:
    #     pickle.dump([strength_pat, conf_pat], f)

    # lconfpat = sorted(conf_pat.items(), key=lambda x: (strength_pat[x[0]]), reverse = True)
    # with open("lconfpat.pkl", "wb") as f:
    #     pickle.dump(lconfpat, f)

    # # l_p_l_s_c = convert_patterns_list(p_s_c)
    # # T, invertList = ConstructPrefixTree(l_p_l_s_c)
    # # SubSump, SubsumW = MineSubsumptions(T, l_p_l_s_c, invertList, 0)
    # # with open('subsumedgeandweight', 'wb') as f:
    # #     pickle.dump([SubSump, SubsumW], f)

    # # N = len(l_p_l_s_c)
    # # dag, caches = DAGcon(SubsumW, N)
    # # with open('dagcaches', 'wb') as f:
    # #     pickle.dump([dag, caches], f)
