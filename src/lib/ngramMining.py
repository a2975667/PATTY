from collections import defaultdict, OrderedDict
from sentence.sentence import Pattern

# from entity_extractor import load_entity
# ets = load_entity()
#from entity import ENTITY_TYPES as ets


def generate_seqmining_dataset(corpus):
    """This function generates a sequence database to mine n-grams from.
    Parameters
    ----------
    patterns : List of Textual Patterns
    Returns
    -------
    type List of Sequences
    """
    
    for tp in corpus.all_textual_pattern:
        tp_words = tp.pattern.split(" ")
        temp = []
        for word in tp_words:
            if word.startswith(tuple([entity+'_' for entity in corpus.entity])):
                if len(temp) != 0:
                    temp = ' '.join(temp)
                    tp.seqmining.append(temp)
                    #smining_dataset.append(temp)
                    temp = []
            else:
                temp.append(word)


def generate_frequent_ngrams(corpus, min_sup):
    """This function mines frequent n-grams from the sequence database

    Parameters
    ----------
    dataset : List of sequences
    min_sup : Minimum support threshold for mining

    Returns
    -------
    Returns a list of n-grams ordered by frequency.

    """
    gen_dict = dict()
    for pattern in corpus.all_textual_pattern:
        for seq in pattern.seqmining:
            raw_pattern = seq.split()
            for i in range(3, 4):
                for j in range(len(raw_pattern) - i + 1):
                    ngram = ' '.join(tuple(raw_pattern[j:j + i]))
                    if ngram in gen_dict:
                        gen_dict[ngram]['count'] += 1
                        for sid in pattern.sentence_id:
                            gen_dict[ngram]['sid'].add(sid)
                    else:
                        gen_dict[ngram] = {
                            'count':1,
                            'sid':set(pattern.sentence_id)
                        }
    gen_dict = {k: v for k, v in gen_dict.items() if v['count'] >= min_sup}
    gen_dict = OrderedDict(sorted(gen_dict.items(), key=lambda t: int(t[1]['count']), reverse=True))
    ngram = []
    for idx, n in enumerate(gen_dict):
        p = Pattern(n,idx)
        p.sentence_id = list(gen_dict[n]['sid'])
        p.count = gen_dict[n]['count']
        ngram.append(p)
    [print(p) for p in ngram]
    corpus.ngram = ngram

    # from pprint import pprint
    # for item in gen_dict:
    #     if gen_dict[item]['count'] >= 5:
    #         print(item, end=' ')
    #         pprint(gen_dict[item])

    # dataset = []
    # x = [pattern.seqmining for pattern in corpus.all_textual_pattern]
    # for i in x:
    #     dataset += i
    # #print(dataset)
    
    # gen_dict = defaultdict(int)
    # for line in dataset:
    # #    print(line)
    #     lst = line.split()
    #     for i in range(3, 4):
    #         for j in range(len(lst) - i + 1):
    #             gen_dict[tuple(lst[j:j + i])] += 1
    # #            print(tuple(lst[j:j + i]))
    # #    print('--------------')
    # fs = {' '.join(k):v for k,v in gen_dict.items() if v >= min_sup}
    # sorted_by_value = sorted(fs.items(), key=lambda kv: (-kv[1], kv[0]))
    # print(sorted_by_value)
    # return sorted_by_value
