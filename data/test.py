
import os

treats = [
    'bacon strip',
    'bread',
    'cheese',
    'chicken tender',
    'chunkers',
    'dentalife',
    'dentastix',
    'fish tender',
    'greenies',
    'liver piece',
    "nature's gift",
    'papadam',
    'peanut butter',
    'roo roll',
    'scrambled egg',
    "tyrell's chip",
    'ultimates beef',
    'ultimates chicken',
    'ultimates lamb',
    'yoghurt'
]

def get_name(i):
    return ' '.join(j for j in i.split()[1:] if not j.startswith(('(','[')))

def get_weight(i):
    return int(i[i.find('(')+1:i.find(')')].strip('g'))

def assert_left_right_pairs(data):
    for pair in data:
        first = [i[0].upper() for i in pair]
        assert first.count('L') == 1
        assert first.count('R') == 1

def assert_valid_treat_names(data):
    for pair in data:
        for item in pair:
            name = get_name(item)
            assert name in treats

def assert_valid_weights(data):
    for pair in data:
        for item in pair:
            weight = get_weight(item)
            assert weight > 0

def assert_single_winners(data, key='[winner]'):
    for pair in data:
        assert sum((key in i) for i in pair) == 1

def assert_no_duplicate_pairs(data):
    pairs = []
    for pair in data:
        pairs.append({i for i in pair})
    for pair in pairs:
        assert pairs.count(pair) == 1

def assert_equal_treats(data):
    items = [get_name(i) for p in data for i in p]
    count = [items.count(i) for i in items]
    assert all(n == count[0] for n in count)

def load_data(root=None):
    data = []

    for file in os.listdir(root):
        if not file.endswith('.txt'):
            continue

        with open(file) as f:
            lines = f.readlines()

        lines = filter(None, (l.strip() for l in lines))

        while any((
            left := next(lines, None),
            right := next(lines, None),
        )):
            data.append((left, right))

    return data

if __name__ == '__main__':
    data = load_data()

    assert_left_right_pairs(data)

    assert_valid_treat_names(data)

    assert_valid_weights(data)

    assert_single_winners(data)

    assert_no_duplicate_pairs(data)

    assert_equal_treats(data)

