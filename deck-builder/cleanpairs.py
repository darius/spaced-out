"""
Given a file of parallel sentences (one pair per line, tab-separated),
filter out the more obviously low-quality pairs.
"""

import re
import sys

def list_words(text):
    text = text.decode('utf8')
    return [word
            for word in re.findall(r'\w+', text.lower(), re.U)
            if not word[0].isdigit()]

for line in sys.stdin:
    line = line.rstrip('\n')
    s, t = line.split('\t')
    sw = list_words(s)
    tw = list_words(t)
    if not sw or not tw or sw == tw:
        continue
    print line
