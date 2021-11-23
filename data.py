import pyconll
import re

class Data:
  def __init__(self, path):
    self.path = path
    self.corpus = corpus = pyconll.iter_from_file(self.path)
    self.sentences = self.extract_sentences()
    self.sentence_texts = self.extract_sentence_texts()
    self.extract_tokens()
    self.token_list = self.extract_tokens()
    self.get_tokens()


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



data = Data("tr_boun-ud-dev.conllu")
print(data.token_list[250])



