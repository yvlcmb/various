"""Normalize the values for seven categories of stats
to determine the greatest basketball player of all time.
This requires the csv files from basketball-reference.com
that consist of total minutes played, total championships, mvp awards,
finals mvp awards, total points scored, total win shares,
total all-league team appearances (1st 2nd and 3rd teams all
counted as one). Each of these are normalized from greatest
to least then finally added all together to generate a total
score. It generates this result:

player,score
Kareem Abdul-Jabbar,5.653529411764706
LeBron James,5.421810637624395
Michael Jordan,5.2576083579942265
Tim Duncan,4.323830102049692
Bill Russell,4.101882382310761
Kobe Bryant,4.072939825908816
Wilt Chamberlain,3.9205862239320814
Karl Malone,3.8722803395765117
Shaquille O'Neal,3.8678193786242208
Julius Erving,3.543067148643215
"""

import csv
from glob import glob
from typing import Dict

import pandas as pd # type: ignore

def normalize(col: pd.Series) -> float:
    """Normalize a column.

    Parameters
    ----------
    col: the column in a dataframe to be normalized

    Returns
    -------
    a float type of the normalized value
    """
    low = col.min()
    rnge = col.max() - low
    return (col - low) / rnge


def normalize_frame(frame: pd.DataFrame, out_col: str, in_col: str) -> tuple:
    """Normalize some column in a data frame of basketball
    stats, then return a two-item tuple, one showing
    player's name and the normalized value.

    Parameters
    ----------
    frame: the dataframe to process
    out_col: the name of the resulting normalized score column
    in_col: the name of the column to normalize
    """
    frame[out_col] = normalize(frame[in_col])
    return tuple(zip(frame['Player'], frame[out_col]))


def rank_all_league(frame: pd.DataFrame,) -> tuple:
    """All-league dataframe requires some extra processing..."""
    frame['totals'] = frame['Tot.1'] + frame['Tot.2']
    return normalize_frame(frame, 'all_league', 'totals')


def rank_finals_mvp(frame: pd.DataFrame,) -> tuple:
    """Finals mvp csv requires some extra steps"""
    temp = frame[['Player', 'Lg']].copy().groupby('Player').count()
    temp['finals_mvp'] = round(temp['Lg'] * 0.166667, 2)
    temp = temp.reset_index()
    return tuple(zip(temp['Player'], temp['finals_mvp']))


def clean_names(frame: pd.DataFrame,) -> None:
    """Strip the asterisks from the player names in a
    basketball stats dataframe"""
    frame['Player'] = frame.Player.str.replace('*', '')


def prep_data(in_dir: str) -> list:
    """"Read files into memory, clean the Player's names
    then return as a list of dataframes."""
    return [clean_names(pd.read_csv(data)) for data in glob(in_dir)]


def process(in_dir: str) -> list:
    """Calculate the greatest basketball player of all time"""
    frames = prep_data(in_dir)

    minutes = normalize_frame(frames[0], 'minutes', 'MP')
    mvps = normalize_frame(frames[1], 'mvps', 'Count')
    finals = rank_finals_mvp(frames[2])
    all_league = rank_all_league(frames[3])
    champs = normalize_frame(frames[4], 'championships', 'Count')
    points = normalize_frame(frames[5], 'points', 'PTS')
    shares = normalize_frame(frames[6], 'winshares', 'WS')

    stats = (minutes, mvps, finals, all_league, champs, points, shares)

    combo: Dict[str, float] = {}
    for stat in stats:
        for player, val in stat:
            if player not in combo:
                combo[player] = 0
            combo[player] += val

    value_key_pairs = ((value, key) for (key, value) in combo.items())
    return sorted(value_key_pairs, reverse=True)


def write_to_disk(in_dir: str) -> bool:
    """Save the results as a .csv file"""
    pairs = process(in_dir)
    rev = [(pair[1], pair[0]) for pair in pairs]
    with open('goat.csv', 'w', newline='', encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['player', 'score'])
        for row in rev:
            if row[1] > 0.0:
                writer.writerow(row)
    return True


if __name__ == "__main__":
    write_to_disk('/home/ike/Documents/basketball/data/*.csv')
