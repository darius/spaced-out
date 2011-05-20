#!/usr/bin/env python3
"""
Wozniak SM-2 algorithm
http://www.supermemo.com/english/ol/sm2.htm
The overall system is not quite clear; this is my interpretation.
"""

import itertools
import json


# Card decks

def load(filename):
    return Deck([parse_card(line.rstrip('\n')) for line in open(filename)])

def parse_card(s):
    return Card(**json.loads(s))

class Deck:

    def __init__(self, cards):
        self.cards = cards

    def get_session_cards(self, date, n_new_cards):
        new_cards = list(itertools.islice(self.unseen_cards(), n_new_cards))
        return new_cards + list(self.due_cards(date))

    def deal(self):
        return min(self.cards, key = lambda card: card.next_showing)

    def save(self, filename):
        f = open(filename, 'w')
        for card in self.cards:
            print(card.as_json(), file=f)

    def unseen_cards(self):
        return (card for card in self.cards if card.next_showing == 0)

    def due_cards(self, date):
        return (card for card in self.cards if 0 < card.next_showing <= date)

class Card:

    def __init__(self, prompt, answer,
                 repetition   = 0,
                 next_showing = 0,
                 interval     = 0,
                 EF           = 2.5):
        self.prompt       = prompt
        self.answer       = answer
        self.repetition   = repetition
        self.next_showing = next_showing
        self.interval     = interval
        self.EF           = EF

    def __repr__(self):
        return 'Card(%s)' % ', '.join('%s=%r' % item
                                      for item in self.__dict__.items())

    def update(self, grade):
        assert grade in range(6)
        if grade < 3:
            self.interval = 1
            self.repetition = 0
        else:
            if self.repetition == 0:
                self.interval = 1
            elif self.repetition == 1:
                self.interval = 6
            else:
                self.interval = int(round(self.interval * self.EF))
            self.repetition += 1
        self.next_showing += self.interval

        self.EF = max(1.3, self.EF - 0.8 + 0.28*grade - 0.02*grade*grade)

    def as_json(self):
        return json.dumps(self.__dict__)


# Anki exports

def convert_anki_export(outfilename, infilename):
    load_anki_export(infilename).save(outfilename)

def load_anki_export(filename):
    return Deck([Card(*line.rstrip('\n').split('\t'))
                 for line in open(filename)])


if False and __name__ == '__main__':
    convert_anki_export('es.deck', 'es.txt')
