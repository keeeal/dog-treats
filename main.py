
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

def normalise_data(treats, pairs):
    wins = get_wins(pairs)
    wins = map(wins.get, treats['NAME'])
    treats['WINS'] = list(wins)
    treats['PRICE'] /= max(treats['PRICE'])
    treats = treats.drop(columns=['NAME'])
    return treats

def print_left_right_bias(pairs):
    print('left wins:', sum(l.winner for l, r in pairs))
    print('right wins:', sum(r.winner for l, r in pairs))

def print_ranking(pairs):
    wins = get_wins(pairs)
    for t in sorted(wins, key=wins.get, reverse=True):
        print(t, wins[t])

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
    structure.remove_edges_below_threshold(0.45)
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

def plot_scatter(data, x, y):
    plot = sns.lmplot(
        x=x, y=y, data=data, palette="muted",
        scatter_kws={"s": 50, "alpha": 1}
    )
    plt.savefig(f'{x}_{y}.png')
    plt.close()

def main():
    treats = load_treats(Path('data') / 'treats.csv')
    pairs = load_pairs(Path('data') / 'pairs')
    data = normalise_data(treats, pairs)

    # print_left_right_bias(pairs)

    print_ranking(pairs)

    plot_correlation(data)

    # plot_causation(data)

    for x in 'CHICKEN', 'HUMANFOOD':
        plot_violin(data, x, 'WINS')

    # for x in 'HARDNESS', 'PROTEIN', 'FAT', 'PRICE':
    #     plot_scatter(data, x, 'WINS')





if __name__ == '__main__':
    main()
