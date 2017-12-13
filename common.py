import string

table = str.maketrans({key: None for key in string.punctuation})

# given a file, get all the words, upper-case each word.
def file_to_words(f):
    lines = f.readlines()
    f.close()
    words = []
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        line_words = line.split(' ')
        for word in line_words:
            word = word.strip().upper()
            word = word.translate(table)
            if word == '':
                continue
            words.append(word)
    return words

