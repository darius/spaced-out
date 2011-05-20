import sys

for line in sorted((line.rstrip('\n')
                    for line in sys.stdin
                    if len(line) < 160),
                   key=len):
    print(line)
