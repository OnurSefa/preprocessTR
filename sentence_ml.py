import pyconll


def prepare_data(file_path):
    data = pyconll.load_from_file(file_path)
    x_value = ''
    y_value = ''

    minimized_list = ['!', '"', '\'', ')', '.', ':', '?']

    for sentence in data._sentences:
        text = sentence.text
        last_char = text[-1]
        if last_char in minimized_list:
            x_value += text
            length = len(text)
            for i in range(length):
                if i == length - 1:
                    y_value += '1'
                else:
                    y_value += '0'
    return x_value, y_value


def train(file_path='tr_boun-ud-train.conllu'):
    x_value, y_value = prepare_data(file_path)

    prior = {}
    likelihood = {}
    total = 0

    for x, y in zip(x_value, y_value):
        char = x
        value = y
        if value == '1':
            try:
                likelihood.update({char: likelihood[char]+1})
            except KeyError:
                likelihood[char] = 1

            try:
                prior.update({value: prior[value]+1})
            except KeyError:
                prior[value] = 1
        else:
            try:
                likelihood.update({char: likelihood[char]})
            except KeyError:
                likelihood[char] = 0

            try:
                prior.update({value: prior[value]+1})
            except KeyError:
                prior[value] = 1

        total += 1

    for p in prior:
        prior.update({p: prior[p]/total})

    length = len(likelihood)
    for l in likelihood:
        likelihood.update({l: (likelihood[l]+1)/(total+length)})

    return prior, likelihood


def test(test_file_path='tr_boun-ud-dev.conllu', train_file_path='tr_boun-ud-train.conllu', limit=0.00001):
    x_value, y_value = prepare_data(test_file_path)
    prior, likelihood = train(train_file_path)

    result = ''
    for x in x_value:
        p = prior['1']
        try:
            like = likelihood[x]
        except KeyError:
            result += '0'
            continue

        probability = p * like
        if probability >= limit:
            result += '1'
        else:
            result += '0'

    return result, y_value


def evaluate(result, y_value):

    precision_correct = 0
    precision_total = 0

    recall_correct = 0
    recall_total = 0

    for r, y in zip(result, y_value):
        if r == '1':
            precision_total += 1
            if y == '1':
                precision_correct += 1
        if y == '1':
            recall_total += 1
            if r == '1':
                recall_correct += 1

    try:
        recall = recall_correct / recall_total
        precision = precision_correct / precision_total
    except ZeroDivisionError:
        return 0, 0

    return precision, recall


if __name__ == '__main__':

    limits = [0.0000001, 0.0000005, 0.000001, 0.000005, 0.00001, 0.00005, 0.0001, 0.0005]
    limits = [0.00001]
    for limit in limits:
        r_result, y_result = test(test_file_path="tr_boun-ud-test.conllu", limit=limit)
        p, r = evaluate(r_result, y_result)

        print('limit:', limit)
        print('precision:', p)
        print('recall:', r)
        print()
