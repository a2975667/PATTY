class Sentence:
    def __init__(self, sentence, sid):
        self.sentence=sentence
        self.textual_patterns = []
        self.sid = sid

    def __str__(self):
        string = str(self.sid) + ': ' + self.sentence
        return string

class Corpus:
    def __init__(self):
        self.corpus = []
        self.count = 0
        self.entity = []
        self.sentence_with_textual_pattern = []
        self.all_textual_pattern = []
    
    def add(self, sentence):
        self.corpus.append(sentence)
        self.count += 1

    def __str__(self):
        string = ''
        for sent in self.corpus:
            string += str(sent)+'\n'
        
        return string
    
    def print_info(self):
        string = 'Corpus have '
        string += str(self.count) +' sentences and entities: '
        string += ' '.join(self.entity)
        print(string)

class Pattern:
    def __init__(self, string, pid):
        self.sentence_id = []
        self.pid = pid
        self.pattern = string
        self.pos = [] # POS of each word
        self.seqmining = [] # sequence from textual_pattern
        self.entity_list=dict()

    def add_id(self, id):
        self.sentence_id.append(id)
    
    def __str__(self):
        return str(self.pid) + ' ' + str(self.sentence_id) + ' ' + self.pattern