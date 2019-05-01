from collections import OrderedDict
from pprint import pprint

def detype(pat, entities):
    words = pat.split(" ")
    strret = list()
    for w in words:
        entity_names = [('<'+entity+'>') for entity in entities]
        if w in entity_names:
            strret.append("<ENTITY>")
        else:
            strret.append(w)
    strret = ' '.join(strret)
    return strret

def get_strength_confidence(p_s_c, utc, corpus):
    strength = dict()
    confidence = dict()
    final = dict()
    for pat in utc:
        strength[pat] = len(utc[pat].entity_list)
        # final[pat] = {}
        # final[pat]['strength'] = len(utc[pat].entity_list)
        # final[pat]['data'] = utc[pat]
    for pat in p_s_c:
        strength[pat] = len(p_s_c[pat].entity_list)
        # final[pat] = {}
        # final[pat]['strength'] = len(p_s_c[pat].entity_list)
        # final[pat]['data'] = utc[p_s_c]
    for pat in p_s_c:
        # confidence[pat] = strength[pat] / strength[(detype(pat, corpus.entity))]
        final[pat] = {}
        final[pat]['confidence'] = strength[pat] / strength[(detype(pat, corpus.entity))]
        final[pat]['data'] = p_s_c[pat]
    
    result = OrderedDict(sorted(final.items(), key=lambda t:t[1]["confidence"], reverse=True))
    
    return result