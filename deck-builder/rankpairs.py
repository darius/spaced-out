#!/usr/bin/env python3
"""
Given a word-frequency table and a flashcard deck, sort the deck in
order of decreasing frequency of the least-frequent word in the card.
Break ties in favor of fewer words.
"""

import math
import re
import sys

counts = dict((word, int(count))
              for line in open('es.vocab')
              for count, word in [line.rstrip('\n').split('\t')])

#print(counts.get('sacar'))
#print(counts.get('la'))
#print(counts.get('basura'))

def rank(card):
    (s1, s2) = card
    s = choose_target_language(s1, s2)
#    print('target', s)
    words = list_words(s)
    if not words:
        return (0, 0, '')
    least_frequent = min(words, key=lambda w: counts.get(w, 0))
    return (counts.get(least_frequent, 0), -len(words), least_frequent)

def choose_target_language(s1, s2):
#    print(s1, cross_entropy(s1))
#    print(s2, cross_entropy(s2))
    return min([s1, s2], key=cross_entropy)

def cross_entropy(s):
    words = list_words(s)
    if not words: return 1000
    return sum(-math.log10(counts.get(w, 1)) for w in words) / len(words)

def count_target_language_words(s):
    words = [w for w in list_words(s) if w in counts]
#    print('words', s, ':', words)
    return len(words)

def list_words(text):
    return [word
            for word in re.findall(r'\w+', text.lower(), re.U)
            if not word[0].isdigit()]

cards = []
for line in sys.stdin:
    card = line.rstrip('\n').split('\t')
    cards.append((rank(card), card))
#    break
cards.sort(reverse=True)

for ((freq, length, word), (prompt, answer)) in cards:
    print(freq, word, prompt, answer, sep='\t')
#    print(prompt, answer, sep='\t')
#for card in cards:
#    print(card)
