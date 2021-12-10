import pyconll
import re


def take_stop_word_list(file_path='stopwords.txt'):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()
    for i, d in enumerate(data):
        data[i] = d[:-1]
    return data


def train(file_path='tr_boun-ud-train.conllu', limit_percentage=150):
    data = pyconll.load_from_file(file_path)
    x_values = []
    frequencies = {}
    total = 0
    for sentence in data._sentences:
        for token in sentence._tokens:
            tag = token.upos
            if tag == 'PUNCT':
                continue
            form = token.form

            if form is None:
                continue

            try:
                frequencies.update({form: frequencies[form] + 1})
            except KeyError:
                frequencies[form] = 1

            total += 1

    value_count = 0
    total_frequency = 0
    for value in frequencies:
        frequency = frequencies[value] / total
        frequencies[value] = frequency
        total_frequency += frequency
        value_count += 1
    mean_frequency = total_frequency / value_count
    limit_frequency = (mean_frequency*limit_percentage)/100

    for value in frequencies:
        if limit_frequency <= frequencies[value]:
            x_values.append(value)

    return x_values


def stop_words(test_file_path='tr_boun-ud-test.conllu', train_file_path='tr_boun-ud-train.conllu', stop_words_list_path='stopwords.txt', limit_frequency_percentage=150):
    list_words = take_stop_word_list(stop_words_list_path)
    train_words = train(train_file_path, limit_percentage=limit_frequency_percentage)
    data = pyconll.load_from_file(test_file_path)
    stopped_words = []
    for sentence in data._sentences:
        for token in sentence._tokens:
            tag = token.upos
            if tag == 'PUNCT':
                continue

            form = token.form

            if form is None:
                continue

            if form in list_words or form in train_words:
                stopped_words.append(form)
                continue

            # if re.search('[^A-Za-z"\']', form) is not None:
                # stopped_words.append(form)
                # continue

    return stopped_words


if __name__ == '__main__':
    deleted = stop_words(limit_frequency_percentage=1500)
    print('a')
