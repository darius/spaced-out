#!/usr/bin/env python3
"""
Make a deck from a parallel corpus.
"""

def lines(filename):
    return (line.rstrip('\n') for line in open(filename))

for s, t in zip(lines('en.sentences'), lines('es.sentences')):
    if s.startswith('<'):
        continue
    print(s, t, sep='\t')
