import pyconll
import re
import numpy as np

class Data:
  def __init__(self, path):
    self.path = path
    self.corpus = corpus = pyconll.iter_from_file(self.path)
    self.sentences = self.extract_sentences()
    self.sentence_texts = self.extract_sentence_texts()
    self.extract_tokens()
    self.token_list = self.extract_tokens()
    self.get_tokens()
    self.sentence_lengths = self.extract_sentence_lengths()
    self.tags = self.initialize_chars()
    self.encode_chars()

  def  extract_sentences(self):
    sentences = []
    for sentence in self.corpus:
        sentences.append(sentence)

    return sentences

  def extract_sentence_texts(self):
      sentence_texts = []
      for sent in self.sentences:
          sentence_texts.append(sent.text)
      return sentence_texts

  def extract_sentence_lengths(self):
      sentence_lengths = []
      for sent in self.sentence_texts:
          sentence_lengths.append(len(sent))
      return sentence_lengths

  def extract_tokens(self):
      token_list = []
      for sentence in self.sentences:
          sent_tokens = sentence._tokens
          matchings = []
          for tok in sent_tokens:
              if re.match(r"[0-9]*-[0-9]*", tok.id):
                  matchings.append(tok.id)
          for matching in matchings:
              match_list = matching.split("-")
              for tkn in sent_tokens:
                  if tkn.id in match_list:
                      sent_tokens.remove(tkn)

          token_list.append(sent_tokens)
      return token_list

  def get_tokens(self):
      for sent in self.token_list:
          for i in range(len(sent)):
              sent[i] = sent[i]._form


  def initialize_chars(self):
      char_tags = []
      for size in self.sentence_lengths:
          tags = []
          for i in range(size):
              tags.append('N')
          char_tags.append(tags)
      return char_tags

  def encode_chars(self):
      # Character tagging 0:N, 1:B, 2:I
      for i in range(len(self.sentences)):
          counter = 0
          for token in self.token_list[i]:
              index = self.sentence_texts[i].find(token, counter)
              if index == -1: continue
              self.tags[i][index] = 'B'
              for j in range(index + 1, index + len(token)):
                  self.tags[i][j] = 'I'
              # sentence_df["char_tags"][i][index+1:index+len(token)] = "I"
              counter = index + len(token)

class MinimizedData(Data):
    def __init__(self,path, mybool, mydict):
        super().__init__(path)
        if self.path == "tr_boun-ud-train.conllu":
            self.sentence_texts.pop(-1)
            self.tags.pop(-1)

        if self.path == "tr_boun-ud-dev.conllu":
            self.sentence_texts.pop(144)
            self.tags.pop(144)
            self.sentence_lengths.pop(144)
        self.sent = self.sentence_texts
        self.char_tags = self.tags
        self.len_sent = len(self.sent)
        self.sents = self.sent_list()
        self.char_to_ix = self.convert_char_to_ix(mybool, mydict)
        self.tag_to_ix = tag_to_ix = {'N': 0, 'B': 1, 'I': 2}
        self.char_index = self.char_indexes()
        self.tag_index = self.tag_indexes()
        self.one_hot = self.one_hot_encoding_chars()
        self.one_hot_tags = self.one_hot_encoding_tags()


    def sent_list(self):
        sents = []
        for i in self.sent:
            sents.append(list(i))
        return sents

    def convert_char_to_ix(self, mybool, mydict):
        if mybool is False:
            return mydict
        else:
            char_to_ix = {}
            for sent in self.sents:
                for char in sent:
                    if char not in char_to_ix:
                        char_to_ix[char] = len(char_to_ix)
            return char_to_ix

    def prepare_sequence(self, seq, idx):
        idxs = [idx[ch] for ch in seq]
        return idxs

    def char_indexes(self):
        char_indexes = []
        for sent in self.sents:
            char_indexes.append(self.prepare_sequence(sent, self.char_to_ix))
        return char_indexes

    def tag_indexes(self):
        tag_indexes = []
        for tag in self.char_tags:
            tag_indexes.append(self.prepare_sequence(tag, self.tag_to_ix))
        return tag_indexes

    def one_hot_encoding_chars(self):
        nb_classes = 103
        one_hots=[]
        for sent in self.char_index:
            targets = sent
            one_hots.append(np.eye(nb_classes)[targets])

        return one_hots

    def one_hot_encoding_tags(self):
        nb_classes = 3
        one_hots = []
        for sent in self.tag_index:
            targets = sent
            one_hots.append(np.eye(nb_classes)[targets])

        return one_hots

mydict = None
data = MinimizedData("tr_boun-ud-train.conllu", True, mydict)
mydict = data.char_to_ix
devdata = MinimizedData("tr_boun-ud-dev.conllu", False, mydict)
print(devdata.len_sent)
'''''
print(devdata.sents[0])
print(devdata.char_tags[0])
print(devdata.len_sent)
print(devdata.char_to_ix)
print(devdata.char_index[1])
print(devdata.tag_index[0])
print(devdata.one_hot_tags[0])
'''''


