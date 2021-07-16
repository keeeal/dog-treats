
from os import name
from pathlib import Path

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from causalnex.structure import notears
from causalnex.plots import plot_structure

from utils.data import load_pairs, load_treats

def discretise(data, n):
    return pd.qcut(data, n, range(n)).astype(int)

def get_wins(pairs):
    items = [i for p in pairs for i in p]
    names = [i.name for i in items]
    return {
        t: sum(i.winner for i in items if i.name == t) / names.count(t)
        for t in set(names)
    }

def add_wins_to_treats(treats, pairs):
    wins = get_wins(pairs)
    wins = map(wins.get, treats['NAME'])
    treats['WINS'] = list(wins)
    return treats

def add_weights_to_treats(treats, pairs):
    items = [i for p in pairs for i in p]
    names = [i.name for i in items]
    order = list(treats['NAME'])
    treats['WEIGHT'] = [
        sum(i.weight for i in items if i.name == t) / names.count(t)
        for t in order
    ]
    return treats

def normalise_treats(treats):
    treats = treats.drop(columns=['NAME'])
    treats['PRICE_100G'] /= max(treats['PRICE_100G'])
    treats['PRICE_ITEM'] /= max(treats['PRICE_ITEM'])
    treats['WEIGHT'] /= max(treats['WEIGHT'])
    return treats

def calculate_prices(treats, pairs):
    items = [i for p in pairs for i in p]
    names = [i.name for i in items]
    order = list(treats['NAME'])
    for i in items:
        i.price = i.weight * treats['PRICE_100G'][order.index(i.name)] / 100
    treats['PRICE_ITEM'] = [
        sum(i.price for i in items if i.name == t) / names.count(t)
        for t in order
    ]
    return treats, pairs

def print_left_right_bias(pairs):
    print('left wins:', sum(l.winner for l, r in pairs))
    print('right wins:', sum(r.winner for l, r in pairs))

def print_ranking(pairs):
    wins = get_wins(pairs)
    for t in sorted(wins, key=wins.get, reverse=True):
        print(t, wins[t])

def print_bill(pairs):
    for pair in pairs:
        for i in pair:
            print()
            print(f'{i.weight}g of {i.name}')
            print(f'\t${i.price:.2f}')

    print(8 * '=')
    print(f'TOTAL:')
    print(f'\t${sum(i.price for p in pairs for i in p):.2f}')

def plot_correlation(data):
    corr = data.corr().stack().reset_index(name="correlation")
    plot = sns.relplot(
        data=corr, palette="vlag",
        x="level_0", y="level_1", hue="correlation", size="correlation",
        hue_norm=(-1, 1), height=7, sizes=(50, 200), size_norm=(-.2, .8),
    )

    plot.set(xlabel='', ylabel='')
    plt.xticks(rotation=90)
    plt.tight_layout(pad=7)
    plt.savefig('correlation.png')
    plt.close()

def plot_causation(data):
    structure = notears.from_pandas(data)
    structure.remove_edges_below_threshold(0.85)
    graph = plot_structure(structure, graph_attributes={'scale': '2.0'})
    graph.draw('structure.png')

def plot_violin(data, x, y):
    data['X'] = len(data[y]) * ['x']
    plot = sns.violinplot(
        data=data, x='X', y=y, hue=x, cut=3,
        split=True, inner="quart", linewidth=1,
        palette='muted'
    )

    sns.despine(left=True)
    plot.set(xlabel='')
    plt.savefig(f'{x}_{y}.png')
    plt.close()

def plot_linear(data, x, y):
    plot = sns.lmplot(
        x=x, y=y, data=data, palette="muted",
        scatter_kws={"s": 50, "alpha": 1}
    )
    plt.savefig(f'{x}_{y}.png')
    plt.close()

def main():
    treats = load_treats(Path('data') / 'treats.csv')
    pairs = load_pairs(Path('data') / 'pairs')
    treats, pairs = calculate_prices(treats, pairs)
    treats = add_weights_to_treats(treats, pairs)
    treats = add_wins_to_treats(treats, pairs)
    treats = normalise_treats(treats)

    # print_bill(pairs)

    # print_left_right_bias(pairs)

    # print_ranking(pairs)

    plot_correlation(treats)

    # plot_causation(treats)

    # for x in 'CHICKEN', 'HUMANFOOD':
    #     plot_violin(treats, x, 'WINS')

    for x in 'HARDNESS', 'PROTEIN', 'FAT', 'PRICE_ITEM', 'WEIGHT':
        plot_linear(treats, x, 'WINS')

if __name__ == '__main__':
    main()
