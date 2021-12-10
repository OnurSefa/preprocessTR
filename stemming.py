import pyconll


def prepare_data(file_path='tr_boun-ud-train.conllu'):
    data = pyconll.load_from_file(file_path)
    y_values = []
    x_values = []

    for sentence in data._sentences:
        for token in sentence._tokens:
            tag = token.upos
            if tag == 'PUNCT':
                continue
            form = token.form
            lemma = token.lemma

            if form is None or lemma is None:
                continue

            y_values.append(lemma)
            x_values.append(form)

    return x_values, y_values


def train(file_path='tr_boun-ud-train.conllu'):
    x_values, y_values = prepare_data(file_path)

    suffixes = []
    dictionary = []
    for x, y in zip(x_values, y_values):
        try:
            y_length = len(y)
            x_length = len(x)
        except TypeError:
            continue
        if x_length <= y_length:
            dictionary.append(x)
            continue
        suffix = x[y_length:x_length]
        word = x[:y_length]
        dictionary.append(word)
        suffixes.append(suffix)

    suffixes.sort(key=lambda a:len(a), reverse=True)
    return suffixes, dictionary


def stemming(test_file_path='tr_boun-ud-test.conllu', train_file_path='tr_boun-ud-train.conllu'):
    suffixes, dictionary = train(train_file_path)
    x_values, y_values = prepare_data(test_file_path)
    x_values = x_values[:100]
    y_values = y_values[:100]

    x_count = len(x_values)
    i = 0
    found_x = []
    compare = []
    while i < x_count:
        x = x_values[i]
        old_x = x
        neu_x = x

        if old_x in dictionary:
            found_x.append(old_x)
            compare.append((old_x, old_x))
            i += 1
            continue

        for suffix in suffixes:
            s_length = len(suffix)
            x_length = len(x)

            if s_length >= x_length - 1:
                continue
            last_part = x[x_length-s_length:]

            if last_part == suffix:
                neu_x = x[:x_length-s_length]
                if neu_x in dictionary:
                    x = x[:x_length-s_length]
                    break
        compare.append((old_x, neu_x))
        i += 1
        found_x.append(x)
        if i % 100 == 0:
            print(i)

    return found_x, y_values, compare


def evaluate(x_values, y_values):
    total = 0
    correct = 0
    for x, y in zip(x_values, y_values):
        if y == None:
            print('a')
            continue
        if x == None:
            print('b')
            continue
        total += 1
        if x == y:
            correct += 1

    accuracy = correct/total
    return accuracy


if __name__ == '__main__':
    x_result, y_result, compare = stemming()
    # a = evaluate(x_result, y_result)
    # print('accuracy:', a)
    print('finished')
