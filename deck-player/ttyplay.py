#!/usr/bin/env python3
"""
TTY interface to sm2.
"""

import codecs
import random
import sys

sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

import ansi
import sm2


def play_extended_session(filename, nsessions, date, n_new_cards):
    deck = sm2.load(filename)
    for d in range(date, date + nsessions):
        play_rounds(deck.get_session_cards(d, n_new_cards))
    deck.save(filename)

def play_session(filename, date, n_new_cards):
    deck = sm2.load(filename)
    play_rounds(deck.get_session_cards(date, n_new_cards))
    deck.save(filename)

def play_rounds(cards):
    play_round(cards, True)
    while cards:
        # TODO: make sure not to repeat a card immediately
        play_round(cards, False)

def play_round(cards, update):
    random.shuffle(cards)
    for card in cards[:]:
        grade = play_card(card)
        if update: card.update(grade)
        if 4 <= grade:
            cards.remove(card)

def play_card(card):
    print(ansi.clear_screen)
    print('Q:', card.prompt)
    input()
    print('A:', card.answer)
    while True:
        print('Your grade? [0..5]', end=' ')
        grade_str = input().strip()
        grade = (int(grade_str) if grade_str else 5)
        if grade in range(6):
            break
    return grade


if __name__ == '__main__':
    play_session('es.deck', 0, 5)
