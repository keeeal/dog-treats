
import os
from pathlib import Path

import pandas as pd

class Item:
    def __init__(self, i: str):
        self.side = i.split(':')[0].upper()
        self.name = ' '.join(j for j in i.split()[1:] if not j.startswith(('(','[')))
        self.weight = int(i[i.find('(')+1:i.find(')')].strip('g'))
        self.winner = '[winner]' in i

def assert_left_right_pairs(data):
    for left, right in data:
        assert left.side == 'L'
        assert right.side == 'R'

# def assert_valid_names(data):
#     for pair in data:
#         for item in pair:
#             assert item.name in TREATS

def assert_valid_weights(data):
    for pair in data:
        for item in pair:
            assert item.weight > 0

def assert_single_winners(data):
    for pair in data:
        assert sum(i.winner for i in pair) == 1

def assert_no_duplicate_pairs(data):
    names = []
    for pair in data:
        names.append({i.name for i in pair})
    for pair in names:
        assert names.count(pair) == 1

def assert_equal_treats(data):
    names = [i.name for p in data for i in p]
    count = [names.count(i) for i in names]
    assert all(n == count[0] for n in count)

def load_pairs(root = None, validate = True):
    data = []

    for file in os.listdir(root):
        if not file.endswith('.txt'):
            continue

        with open(Path(root) / file) as f:
            lines = f.readlines()

        lines = filter(None, (l.strip() for l in lines))

        while any((
            left := next(lines, None),
            right := next(lines, None),
        )):
            data.append((Item(left), Item(right)))

    if validate:
        assert_left_right_pairs(data)
        # assert_valid_names(data)
        assert_valid_weights(data)
        assert_single_winners(data)
        assert_no_duplicate_pairs(data)
        assert_equal_treats(data)

    return data

def load_treats(csv_file):
    return pd.read_csv(csv_file)
