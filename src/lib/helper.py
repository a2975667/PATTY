import networkx as nx
import spacy
import sys
import pickle
nlp = spacy.load('en_core_web_sm')

#helper funtion to check entities
def check_entities(sentence, ets):
    possible_entities = list(ets)
    sentence_words = sentence.split(" ")
    total_present = 0
    entities_present = []
    for ent in possible_entities:
        result = [word for word in sentence_words if ent in word]
        if len(result) > 0:
            result = set(result)
            total_present += len(result)
            entities_present.extend(list(result))
    return total_present, entities_present


def shortest_dependency_path(doc, e1=None, e2=None):
    edges = []
    for token in doc:
        for child in token.children:
            edges.append(('{0}'.format(token),
                          '{0}'.format(child)))
    graph = nx.Graph(edges)
    try:
        shortest_path = nx.shortest_path(graph, source=e1, target=e2)
    except nx.NetworkXNoPath:
        shortest_path = []
    return shortest_path

def adv_mod_deps(x, dep_parse):
    for token in dep_parse:
        if token.dep_ == "advmod":
            for word in x:
                if str(token) == word:
                    x.insert(x.index(str(token)), str(token.head.text))
                    break
                if str(token.head.text) == word:
                    x.insert(x.index(str(token.head.text)), str(token))
                    break
    return x

def generate_pos_tags_for_patterns(corpus):

    post = list()
    i = 0
    all_pattern = []
    all_pos = []
    counter = 0
    for pattern in corpus.all_textual_pattern:

        sys.stderr.write('Processing...{0:.3%}\r'.format(counter/len(corpus.all_textual_pattern)))
        counter += 1

        all_pattern.append(pattern.pattern)

        dep = nlp(pattern.pattern)
        pos_tag = [t.pos_ for t in dep]
        pattern.pos = pos_tag
        all_pos.append(pos_tag)

    with open('TexPatPosTag.pkl', 'wb') as f:
        pickle.dump([all_pattern, all_pos], f)
    return post
