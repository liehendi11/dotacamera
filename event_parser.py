import math

import pandas as pd
from tqdm import tqdm

from events import Event
import sys

"""
Death
1. Hero x hero (hero killed other hero)
2. Creep x hero (LOL territory)
3. Tower x hero
4. Neutral x hero
5. Roshan x hero
6. Hero x creep
7. Hero x tower
8. Hero x neutral
9. Hero x roshan


Damage
Interaction handled:
1. Hero x hero (hero give damage to other hero)
2. Creep x hero (creep give damage to a hero)
3. Tower x hero
4. Neutral x hero
5. Roshan x hero
6. Hero x creep
7. Hero x tower
8. Hero x neutral
9. Hero x hero
10. Hero x roshan

Order of importance (hero to ...)
KILL
Hero D, Roshan kill hero, tower kill hero, Roshan D, Tower D, Neutral D, Creep D, 
60      60                60               60        40       7          2

DAMAGE
Hero, tower, creep, neutral, roshan, self hurt
3     2      1      2        3       1

"""

value_parameter = [
    ("damage", "hero", "hero", 3, 60, 60),  # hero x hero damage
    ("damage", "hero", "tower", 2, 60, 60),  # hero x tower damage
    ("damage", "hero", "creep", 1, 60, 60),  # hero x creep damage
    ("damage", "hero", "neutral", 3, 60, 60),  # hero x neutral damage
    ("damage", "hero", "roshan", 1, 60, 60),  # hero x roshan damage
    ("damage", "hero", float('nan'), 1, 60, 60),
    ("death", "hero", "hero", 60, 150, 120),  # hero x hero death
    ("death", "hero", "tower", 40, 120, 120),  # hero x tower death
    ("death", "hero", "creep", 2, 60, 60),  # hero x creep death
    ("death", "hero", "neutral", 6, 75, 75),  # hero x neutral death
    ("death", "roshan", "hero", 70, 150, 120),  # hero x roshan death
    ("death", "tower", "hero", 40, 120, 90),
]

tick_interval = 15

def get_value_param(log):
    for val in value_parameter:
        if val[0] == log['event'] and val[1] == log['primary_target'] and val[2] == log['secondary_target']:
            return val

    return -1

def get_event_values(tick):
    res = {
        "hero_0": 0,
        "hero_1": 0,
        "hero_2": 0,
        "hero_3": 0,
        "hero_4": 0,
        "hero_5": 0,
        "hero_6": 0,
        "hero_7": 0,
        "hero_8": 0,
        "hero_9": 0,
        "roshan": 0,
        "tower_0": 0,
        "tower_1": 0,
        "tower_2": 0,
        "tower_3": 0,
        "tower_4": 0,
        "tower_5": 0,
        "tower_6": 0,
        "tower_7": 0,
        "tower_8": 0,
        "tower_9": 0,
        "tower_10": 0,
        "tower_11": 0,
        "tower_12": 0,
        "tower_13": 0,
        "tower_14": 0,
        "tower_15": 0,
        "tower_16": 0,
        "tower_17": 0,
        "tower_18": 0,
        "tower_19": 0,
        "tower_20": 0,
        "tower_21": 0
    }

    for event in events:
        if (tick < event.min_tick) or (tick > event.max_tick): continue
        val_dict = event.get_future_values(tick, tick_interval)

        for k in val_dict:
            if k in res:
                res[k] += val_dict[k]

    max_k = max(res, key=res.get)
    res['target'] = max_k
    res['tick'] = tick

    return res

if __name__ == '__main__':
    """
    Run this with "python event_parser.py [1] [2] [3]"
    Input files required (2):
    1. X_df: hero position, etc
    2. Parsed events
    
    Output files (1):
    3. Y
    """

    if len(sys.argv) != 4:
        print("Wrong parameters supplied. Exiting...")
        exit(1)

    X_df = pd.read_csv(sys.argv[1])
    parsed_events_df = pd.read_csv(sys.argv[2])

    # parse events
    events = []
    for i, row in tqdm(parsed_events_df.iterrows()):
        rowd = dict(row)

        val = get_value_param(rowd)
        if (val == -1): continue

        name_1 = rowd['primary_target']
        if not math.isnan(rowd['primary_target_idx']):
            name_1 += "_{}".format(int(rowd['primary_target_idx']))

        name_2 = rowd['secondary_target']
        if not math.isnan(rowd['secondary_target_idx']):
            name_2 += "_{}".format(int(rowd['secondary_target_idx']))

        events.append(Event(rowd['tick'], val[3], val[4], val[5], name_1, name_2))

    # produce Y values
    print("Ready to calculate!")
    ticks = list(X_df['tick'])
    y = []
    for tick in tqdm(ticks):
        y.append(get_event_values(tick))

    df_y = pd.DataFrame(y, columns=y[0].keys())
    df_y.to_csv(sys.argv[3])


