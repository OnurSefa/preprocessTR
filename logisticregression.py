import data
from sklearn.linear_model import LogisticRegression
import numpy as np

'''''
X, y = load_iris(return_X_y=True)
>>> clf = LogisticRegression(random_state=0).fit(X, y)
'''''
mydict = None
train_data = data.MinimizedData("tr_boun-ud-train.conllu", True, mydict)
mydict = train_data.char_to_ix
dev_data = data.MinimizedData("tr_boun-ud-dev.conllu", False, mydict)
x_train = np.array(train_data.one_hot)
y_train = np.array(train_data.tag_index)

deneme = np.array(train_data.char_index[0])

x_test = np.array(dev_data.one_hot)
y_test = np.array(dev_data.tag_index)
dev_token_list = np.array(dev_data.token_list)
print(len(dev_token_list))

zipped_dev = []
for i in range(len(x_test)):
    zipped_dev.append(list(zip(x_test[i], y_test[i])))

flat_list_dev = [item for sublist in zipped_dev for item in sublist]

dev_x = []
dev_y = []
for key,value in flat_list_dev:
    dev_x.append(key)
    dev_y.append(value)

#karakterleri tagleriyle birlikte birer birer ver




zipped = []
for i in range(len(x_train)):
    zipped.append(list(zip(x_train[i], y_train[i])))



flat_list = [item for sublist in zipped for item in sublist]


train_x = []
train_y = []
for key,value in flat_list:
    train_x.append(key)
    train_y.append(value)





train_x = np.array(train_x)




clf = LogisticRegression(class_weight="balanced", solver="lbfgs", penalty="l2").fit(train_x, train_y)
print(len(x_test[0]))
y_pred = LogisticRegression.predict(self= clf, X=dev_x)



sentence_lengths = dev_data.sentence_lengths

print(sentence_lengths[1])
lens = []
for i in range(len(dev_data.sents)):
    char_list = []
    len_sent = len(dev_data.sents[i])
    lens.append(len_sent)

print(len(dev_data.sents))

count = 0
sent_list = []
for j in lens:
    char_list = []
    for x in range(count, j, 1):
        char_list.append(y_pred[x])
    sent_list.append(char_list)


index_list_1 = []
index_list_2 = []
item = 1
for element in sent_list:
    indexes = [index for index, v in enumerate(element) if v == 1]
    indexes_2 = [index for index, v in enumerate(element) if v == 2]
    index_list_1.append(indexes)
    index_list_2.append(indexes_2)
print(index_list_1[0])

sentences = dev_data.sents

predicted_tokens = []
for s in range(len(index_list_1)):
    tokens = []
    for ind in range(len(index_list_1[s])):
        index_1 = index_list_1[s][ind]
        if ind+1 < len(index_list_1[s]):
            next_ind = index_list_1[s][ind+1]
            token = sentences[s][index_1: next_ind]
            if token[-1] == ' ':
                token.pop(-1)
        else:
            token = sentences[s][index_1:]

        token = "".join(token)
        tokens.append(token)
    predicted_tokens.append(tokens)

print(sent_list[0])
print(predicted_tokens[0])
print(sent_list[56])
print(predicted_tokens[56])


correct_count = 0

for i in range(len(predicted_tokens)):
    for j in range(len(dev_data.token_list)):
        pred_tokens = predicted_tokens[i]
        act_tokens = dev_data.token_list[j]
        if len(act_tokens) >= len(pred_tokens):
            for ind in range(len(pred_tokens)):
                if pred_tokens[ind] == act_tokens[ind]:
                    #print(pred_tokens[ind])
                    correct_count +=1
        else:
            for ind in range(len(act_tokens)):
                if pred_tokens[ind] == act_tokens[ind]:
                    #print(pred_tokens[ind])
                    correct_count +=1

print(correct_count)

all_count = 0
for listElem in dev_data.token_list:
    all_count += len(listElem)

print(all_count)

print("accuracy: " ,correct_count/all_count)






