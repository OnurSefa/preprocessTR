import pyconll


def prepare_data(file_path='./tr_boun-ud-dev.conllu'):
    dev = pyconll.load_from_file(file_path)
    y_value = ''
    x_value = ''
    for sentence in dev._sentences:
        x_value += sentence.text
        y_value += sentence.text
        y_value += chr(126)
    y_value = y_value[:-1]

    return x_value, y_value


def prepare_data_corrected(file_path='./tr_boun-ud-dev.conllu'):
    dev = pyconll.load_from_file(file_path)
    y_value = ''
    x_value = ''

    accepted_last_char_list = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<',
                               '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

    minimized_list = ['!', '"', '\'', ')', '.', ':', '?']

    for sentence in dev._sentences:
        text = sentence.text
        last_char = text[-1]
        if last_char in minimized_list:
            x_value += sentence.text
            y_value += sentence.text
            y_value += chr(126)
    y_value = y_value[:-1]

    return x_value, y_value


def sentence_splitter(x_data):

    split = False
    y_hat = ''
    inside_quotation = False
    inside_single_quotation = False
    inside_parenthesis = False
    length = len(x_data)
    for i, c in enumerate(x_data):
        value = ord(c)
        if value == 34:
            if inside_quotation:
                inside_quotation = False
            else:
                inside_quotation = True
        if value == 39:
            if inside_single_quotation:
                inside_single_quotation = False
            else:
                inside_single_quotation = True
        if value == 40:
            inside_parenthesis = True
        if value == 41:
            inside_parenthesis = False

        if not(inside_quotation or inside_single_quotation or inside_parenthesis):
            if i < length - 1:
                if value == 46:
                    if ord(x_data[i+1]) == 46:
                        split = False
                    else:
                        split = True
                if value == 33:
                    split = True
                if value == 63:
                    split = True

        y_hat += c
        if split:
            y_hat += chr(126)
            split = False

    return y_hat


def sentence_splitter_corrected(x_data):

    split = False
    y_hat = ''
    inside_quotation = False
    inside_single_quotation = False
    inside_parenthesis = False
    length = len(x_data)
    for i, c in enumerate(x_data):
        value = ord(c)
        if value == 34:
            if inside_quotation:
                inside_quotation = False
            else:
                inside_quotation = True
        if value == 39:
            if inside_single_quotation:
                inside_single_quotation = False
            else:
                inside_single_quotation = True
        if value == 40:
            inside_parenthesis = True
        if value == 41:
            inside_parenthesis = False

        if i < length - 1:
            if value == 46:
                if ord(x_data[i + 1]) == 46:
                    split = False
                else:
                    split = True
            if value == 33:
                split = True
            if value == 63:
                split = True

        y_hat += c
        if split:
            y_hat += chr(126)
            split = False

    return y_hat


def evaluate(y_given, y_found):

    precision_correct = 0
    precision_total = 0

    recall_correct = 0
    recall_total = 0

    """if given_length > found_length:
        for i in range(given_length-found_length):
            y_found += ' '
    if found_length > given_length:
        for i in range(found_length-given_length):
            y_given += ' '"""

    length = len(y_found)
    g = 0
    f = 0
    while f < length:
        f_value = ord(y_found[f])
        g_value = ord(y_given[g])

        if f_value == 126:
            precision_total += 1
            if g_value == 126:
                precision_correct += 1
                g += 1
                f += 1
            else:
                f += 1
        elif g_value == 126:
            g += 1
        else:
            g += 1
            f += 1

    precision = precision_correct / precision_total

    length = len(y_given)
    g = 0
    f = 0

    while g < length:
        f_value = ord(y_found[f])
        g_value = ord(y_given[g])

        if g_value == 126:
            recall_total += 1
            if f_value == 126:
                recall_correct += 1
                g += 1
                f += 1
            else:
                g += 1
        elif f_value == 126:
            f += 1
        else:
            g += 1
            f += 1

    recall = recall_correct / recall_total

    return precision, recall


if __name__ == '__main__':

    x, y = prepare_data()
    y_hat = sentence_splitter(x)
    p, r = evaluate(y, y_hat)

    print('precision:', p)
    print('recall:', r)

    x, y = prepare_data_corrected()
    y_hat = sentence_splitter_corrected(x)
    p, r = evaluate(y, y_hat)

    print('corrected precision:', p)
    print('corrected recall:', r)
