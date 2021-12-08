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

            if form == None or lemma == None:
                continue

            y_values.append(lemma)
            x_values.append(form)

    return x_values, y_values


def train(file_path='tr_boun-ud-train.conllu'):
    x_values, y_values = prepare_data(file_path)

    suffixes = []
    for x, y in zip(x_values, y_values):
        try:
            y_length = len(y)
            x_length = len(x)
        except TypeError:
            continue
        if x_length <= y_length:
            continue
        suffix = x[y_length:x_length]
        suffixes.append(suffix)

    suffixes.sort(key=lambda a:len(a), reverse=True)

    return suffixes


def train_strategy2(file_path='tr_boun-ud-train.conllu'):
    x_values, y_values = prepare_data(file_path)

    suffixes2 = []
    suffixes1 = []
    suffixes0 = []
    for x, y in zip(x_values, y_values):
        try:
            y_length = len(y)
            x_length = len(x)
        except TypeError:
            continue
        if x_length <= y_length:
            continue
        suffix = x[y_length:x_length]
        suffixes0.append(('', suffix))
        if x_length > y_length:
            last_one = x[y_length-1:y_length]
            suffixes1.append((last_one, suffix))
        if x_length-1 > y_length:
            last_two = x[y_length-2:y_length]
            suffixes2.append((last_two, suffix))

    suffixes0.sort(key=lambda a:len(a[1]), reverse=True)
    suffixes1.sort(key=lambda a:len(a[1]), reverse=True)
    suffixes2.sort(key=lambda a:len(a[1]), reverse=True)

    return suffixes1


def train_strategy3(file_path='tr_boun-ud-train.conllu'):
    x_values, y_values = prepare_data(file_path)

    suffixes = []
    for x, y in zip(x_values, y_values):
        try:
            y_length = len(y)
            x_length = len(x)
        except TypeError:
            continue
        if x_length <= y_length:
            continue
        suffix = x[y_length:x_length]
        suffixes.append(suffix)

    result = []
    length = len(suffixes)
    for index, s in enumerate(suffixes):
        if len(s) == 0:
            continue
        for i in range(length):
            if index == i:
                continue
            inspect = suffixes[i]
            inspect_length = len(inspect)
            s_length = len(s)
            if inspect_length < s_length:
                continue
            last_part = inspect[inspect_length-s_length:]
            if last_part == s:
                suffixes[i] = inspect[:inspect_length-s_length]

    for s in suffixes:
        if len(s) > 0:
            result.append(s)
    return result


def train_strategy4(file_path='tr_boun-ud-train.conllu'):
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


def test(test_file_path='tr_boun-ud-test.conllu', train_file_path='tr_boun-ud-train.conllu'):
    suffixes = train(train_file_path)
    # suffixes = train_strategy2(train_file_path)
    x_values, y_values = prepare_data(test_file_path)

    x_count = len(x_values)
    i = 0
    found_x = []
    compare = []
    while i < x_count:
        x = x_values[i]
        old_x = x
        neu_x = x
        for suffix in suffixes:
            s_length = len(suffix)
            # last_two = suffix[0]
            x_length = len(x)

            if s_length > x_length - 3:
                continue
            last_part = x[x_length-s_length:]
            # end = x[x_length-s_length-2:x_length-s_length]

            # if end == last_two:
            if last_part == suffix:
                neu_x = x[:x_length-s_length]
                x = x[:x_length-s_length]
                break
        compare.append((old_x, neu_x))
        i += 1
        found_x.append(x)
        if i % 1000 == 0:
            print(i)

    return found_x, y_values, compare


def test_strategy4(test_file_path='tr_boun-ud-test.conllu', train_file_path='tr_boun-ud-train.conllu'):
    suffixes, dictionary = train_strategy4(train_file_path)
    x_values, y_values = prepare_data(test_file_path)
    x_values = x_values[:200]
    y_values = y_values[:200]

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


def test_strategy2(test_file_path='tr_boun-ud-test.conllu', train_file_path='tr_boun-ud-train.conllu'):
    suffixes = train_strategy2(train_file_path)
    x_values, y_values = prepare_data(test_file_path)
    x_values = x_values[:2000]
    y_values = y_values[:2000]

    x_count = len(x_values)
    i = 0
    found_x = []
    compare = []
    while i < x_count:
        x = x_values[i]
        old_x = x
        neu_x = x
        for suffix in suffixes:
            s_length = len(suffix[1])
            last_two = suffix[0]
            x_length = len(x)

            if s_length > x_length - 1:
                continue
            last_part = x[x_length-s_length:]
            end = x[x_length-s_length-1:x_length-s_length]

            if end == last_two:
                if last_part == suffix:
                    neu_x = x[:x_length-s_length]
                    x = x[:x_length-s_length]
                    break
        compare.append((old_x, neu_x))
        i += 1
        found_x.append(x)
        if i % 200 == 0:
            print(i)

    return found_x, y_values, compare


def test_strategy3(test_file_path='tr_boun-ud-test.conllu', train_file_path='tr_boun-ud-train.conllu'):
    suffixes = train_strategy3(train_file_path)
    x_values, y_values = prepare_data(test_file_path)
    x_values = x_values[:2000]
    y_values = y_values[:2000]

    x_count = len(x_values)
    i = 0
    found_x = []
    while i < x_count:
        cont = True
        x = x_values[i]
        for suffix in suffixes:
            s_length = len(suffix)
            x_length = len(x)

            if s_length < 1:
                continue

            if s_length > x_length - 2:
                continue
            last_part = x[x_length-s_length:]

            if last_part == suffix:
                x = x[:x_length-s_length]
                x_values[i] = x
                cont = False
                break
        if cont:
            i += 1
            found_x.append(x)
        if i % 200 == 0:
            print(i)
    compare = []
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
    x_result, y_result, compare = test_strategy4()
    a = evaluate(x_result, y_result)
    print('accuracy:', a)
    print('a')
