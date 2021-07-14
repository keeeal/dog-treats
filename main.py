
from utils.data import load_pairs, load_treats
from pathlib import Path

def print_left_right_bias(data):
    print('left wins:', sum(l.winner for l, r in data))
    print('right wins:', sum(r.winner for l, r in data))

def print_ranking(data, treats):
    wins = {
        t: sum(i.winner for p in data for i in p if i.name == t)
        for t in treats
    }

    ranking = sorted(treats, key=wins.get, reverse=True)
    names = [i.name for p in data for i in p]

    for treat in ranking:
        print(f'{treat}: {100 * wins.get(treat) / names.count(treat)}%')

def main():
    data = load_pairs(Path('data') / 'pairs')
    treats = load_treats(Path('data') / 'treats.csv')
    names = list(treats['NAME'])

    # print_left_right_bias(data)

    print_ranking(data, names)

if __name__ == '__main__':
    main()
