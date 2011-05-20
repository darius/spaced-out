"""
Print a table of all words in a corpus with their frequencies,
in decreasing order of frequency.
"""

import re

def rank_words(file):
    return sorted(((count, word)
                   for word, count in count_words(file).iteritems()),
                  reverse=True)

def count_words(file):
    counts = {}
    for word in all_words(file):
        counts[word] = counts.get(word, 0) + 1
    return counts

def all_words(file):
    for line in gen_lines(file):
        for word in gen_words(line):
            if not word.isdigit():
                yield word.lower()

def gen_lines(file):
    return (line.rstrip('\n') for line in file)

def gen_words(text):
    return re.findall(r"\w+", text.decode('utf8'), re.U)

if __name__ == '__main__':
    if False:
        for line in gen_lines(open('es.corpus')):
            for word in gen_words(line):
                print word.encode('utf8')
    for count, word in rank_words(open('es.corpus')):
        print '%d\t%s' % (count, word.encode('utf8'))
