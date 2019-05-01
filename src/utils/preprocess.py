from utils.entity_extractor import extract_entity, dump_entity, load_entity
from sentence.sentence import Sentence, Corpus

def read_corpus(file):
    corpus = Corpus()
    with open(file, 'rb') as f:
        for idx, line in enumerate(f):
            line = line.strip()
            line = str(line,'utf-8')
            sentence = Sentence(line, idx)
            # print(sentence)
            corpus.add(sentence)
    return corpus

def preprocess(params):
    print("Reading Corpus...")
    print("Generating entity sets...")
    print(params)
    
    #dump_entity(params['corpus_fn'])
    entity = extract_entity(params['corpus_fn'])
    #print("found", load_entity())
    print("found", entity)
    print("Processing Corpus...")
    corpus = read_corpus(params['corpus_fn'])
    corpus.entity = entity
    return corpus