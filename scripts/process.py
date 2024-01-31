import sys 
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain
from collections import Counter
import re

def proccess_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=',')

    my_df = pd.DataFrame()
    my_df['playerwin'] = df['winloss'].apply(lambda x: 1 if x == 'Win' else 0)
    my_df['blackjack'] = df['blkjck'].apply(lambda x: 1 if not x == 'nowin' else 0) * my_df['playerwin']
    my_df['bust'] = df['plybustbeat']
    my_df['ply2cardsum'] = df['ply2cardsum']

    my_df['cards'] = df.apply(lambda x: [
        x['card1'], x['card2'], x['card3'], x['card4'], x['card5']
        ], axis=1)
    my_df['dealcards'] = df.apply(lambda x: [
        x['dealcard1'], x['dealcard2'], x['dealcard3'], x['dealcard4'], x['dealcard5']
        ], axis=1)

    my_df['cards'] = my_df['cards'].apply(lambda x: [c for c in x if c != 0])
    my_df['dealcards'] = my_df['dealcards'].apply(lambda x: [c for c in x if c != 0])
    return my_df

def win_prob_2sum(df: pd.DataFrame, savepath: str):
    avg_prob_by_sum = df.groupby('ply2cardsum')['playerwin'].mean()

    plt.figure(figsize=(10, 6))
    plt.plot(avg_prob_by_sum.index, avg_prob_by_sum.values, marker='o', linestyle='-')
    plt.title('Average Probability of Player Winning by Sum of First 2 Cards')
    plt.xlabel('Sum of First 2 Cards')
    plt.ylabel('Average Probability of Winning')
    plt.xticks(range(1, 22))
    plt.ylim(0, 1)
    plt.grid(True)
    plt.savefig(savepath)
    plt.clf()
  
def card_prob(df: pd.DataFrame, savepath: str):
    player_cards_flat = list(chain.from_iterable(df['cards'].values))
    player_cards_num = len(player_cards_flat)
    player_card_prob = Counter(player_cards_flat)
    x = np.array(list(player_card_prob.keys()))
    player_y = np.array(list(player_card_prob.values())) / player_cards_num

    dealer_cards_flat = list(chain.from_iterable(df['dealcards'].values))
    dealer_cards_num = len(dealer_cards_flat)
    dealer_card_prob = Counter(dealer_cards_flat)
    dealer_x = np.array(list(dealer_card_prob.keys()))
    dealer_y = np.array(list(dealer_card_prob.values())) / dealer_cards_num

    bar_width = 0.35
    plt.bar(x - bar_width/2, player_y, color='blue', width=bar_width, label='Player cards')
    plt.bar(dealer_x + bar_width/2, dealer_y, color='red', width=bar_width, label='Dealer cards')

    plt.xlabel('Cards')
    plt.ylabel('Probability')
    plt.title('Density chart')
    plt.xticks(range(1, 12))
    plt.yticks(np.arange(0, 0.34, 0.02))
    plt.grid(True, axis='y')

    plt.legend()
    plt.savefig(savepath)
    plt.clf()

def win_amount(df: pd.DataFrame, savepath: str):
    win_amounts = ((df['playerwin'] * 2 - 1) * (df['blackjack'] * df['playerwin'] * 0.5 + 1)) * 100
    average_win_amount = win_amounts.mean()
    plt.figure(figsize=(5, 6))

    plt.boxplot(win_amounts, widths=0.7)
    plt.hlines(average_win_amount, 0.65, 1.35, colors='green', label='Average')

    plt.title('Boxplot of Win Amounts for a $100 Bet')
    plt.xlabel('Win Amount')
    plt.xticks([])
    plt.yticks([i for i in range(-150, 151, 10)])
    plt.grid(True, axis='x')

    plt.legend()
    plt.savefig(savepath)
    plt.clf()

def bust_freq(df: pd.DataFrame, savepath: str):
    bust_value_counts = df['bust'].value_counts()
    player_bust = bust_value_counts['Bust'] / df.shape[0]
    dealer_bust = bust_value_counts['DlBust'] / df.shape[0]
    player_blkjck = df['blackjack'].mean()

    plt.figure(figsize=(10, 6))
    plt.bar('Player Bust', player_bust, color='orange')
    plt.bar('Dealer Bust', dealer_bust, color='green')
    plt.bar('Player Blackjack', player_blkjck, color='black')
    plt.title('Probabilities')
    plt.ylim(0, 0.4)
    plt.grid(True)

    plt.savefig(savepath)
    plt.clf()

def myformat_to_df(filepath: str) -> pd.DataFrame:
    myformat_regexp = r'(.*?),(.*?),(.*?),(.*?),\[(.*?)\],\[(.*?)\]'

    lines = []
    with open(filepath, 'r') as file:
        lines = file.readlines()

    headers = lines[0][:-1].split(',')
    data = [re.search(myformat_regexp, line) for line in lines[1:]]

    data = dict([(header, [row.group(i+1) for row in data[:]]) for i, header in enumerate(headers)])

    df = pd.DataFrame(data)
    df['playerwin'] = df['playerwin'].astype(int)
    df['blackjack'] = df['blackjack'].astype(int)
    df['ply2cardsum'] = df['ply2cardsum'].astype(int)
    df['cards'] = df['cards'].apply(lambda x: [int(i) for i in x.split(',')])
    df['dealcards'] = df['dealcards'].apply(lambda x: [int(i) for i in x.split(',')])

    return df

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: dataset_csv output_folder')
        exit(-1)

    dataset_csv, output_folder = sys.argv[1], sys.argv[2]
    if not os.path.isfile(dataset_csv) or not os.path.isdir(output_folder):
        print('Nonexisting dataset_csv or output_folder paths')
        exit(-2)

    if dataset_csv.endswith('.myformat'):
        df = myformat_to_df(dataset_csv)
    elif dataset_csv.endswith('.csv'):
        df = proccess_csv(dataset_csv)
    else:
        print('Unsupported dataset format')
        exit(-3)

    win_prob_2sum(df, os.path.join(output_folder, 'win_prob.pdf'))
    card_prob(df, os.path.join(output_folder, 'card_prob.pdf'))
    win_amount(df, os.path.join(output_folder, 'win_amount.pdf'))
    bust_freq(df, os.path.join(output_folder, 'bust_freq.pdf'))

