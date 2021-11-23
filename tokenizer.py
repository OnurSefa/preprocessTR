import sentence_splitter
import pandas as pd
import data
from sklearn.linear_model import LogisticRegression
import re

def tokenizer(text):
    abb_list = ['Dr.', 'Dt.', 'Av.', 'Prof.']
    text_list = list(text)
    for i in range(len(text_list)):
        if text_list[i]=='.':
            #if end of sentence
            if i==(len(text_list)-1):
                text_list[i]=' .'
            elif text_list[i+1] == '\"':
                text_list[i] = ' .'
        if text_list[i] == ',':
            text_list[i] = ' , '
        if text_list[i] == '\'':
            text_list[i] = '\''
        if text_list[i] == ':':
            text_list[i] = ' :'
        if text_list[i] == ';':
            text_list[i] = ' ;'
        if text_list[i] == '!':
            text_list[i] = ' !'
        if text_list[i] == '?':
            text_list[i] = ' ?'
        if text_list[i] == '-':
            text_list[i] = ' - '
        if text_list[i] == '(':
            text_list[i] = ' ( '
        if text_list[i] == ')':
            text_list[i] = ' ) '
        if text_list[i] == '\"':
            text_list[i] = ' \" '
            print(text_list[i])

    new_text= ''.join(text_list)

    split_by_whitespace = new_text.split()
    return split_by_whitespace


def evaluate_tokenizer(data):
    '''
    precision = TruePositives/ (TruePositives + FalsePositives)
    recalL = TruePositives / (TruePositives + FalseNegatives)
    '''


    actual_token_list = data.token_list
    tokenized_data = []
    correct = 0
    total = 0

    for sent in data.sentence_texts:
        tokenized_data.append(tokenizer(sent))


    for s in range(len(tokenized_data)):
        if s < len(actual_token_list):
            for i in range(len(tokenized_data[s])):
                if i<len(actual_token_list[s]):
                    if actual_token_list[s][i] == tokenized_data[s][i]:
                        correct +=1
                    else:
                        print(tokenized_data[s])
                        print(actual_token_list[s])


    #print(tokenized_data)
    for item in actual_token_list:
        for x in item:
            total+=1

    return correct/total
''' 
def process_data(data):
    x_data = []
    for s in range(len(data.sentence_texts)):
        x_data.append(list(data.sentence_texts[s]))
        for t in range(len(data.token_list[s])):
            for t

    y_data = []


    print(x_data)


def log_reg_tokenizer(train_data, test_data):
    x_train = "Buse geldi."
    y_train = pd.get_dummies(["Buse", "geldi", "."])

    x_test = test_data.sentence_texts
    y_test = test_data.token_list

    #print(x_test)


    logisticRegr = LogisticRegression()


    #training the classifier
    logisticRegr.fit(x_train, y_train)
    
    #predict
    y_pred = logisticRegr.predict(x_test)
    print(y_pred)
   

    #score
    score = logisticRegr.score(x_test, y_test)
    print(score)
'''



train_data = data.Data("tr_boun-ud-train.conllu")
test_data = data.Data("tr_boun-ud-test.conllu")
data = data.Data("tr_boun-ud-test.conllu")
#process_data(data)
print(data.sentence_texts[-1])
eval = evaluate_tokenizer(data)
print(eval)
#log_reg_tokenizer(train_data, test_data)
print(tokenizer(""))
