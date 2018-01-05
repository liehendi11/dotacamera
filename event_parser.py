import math

import pandas as pd
from tqdm import tqdm

from events import Event
import sys
import numpy as np

from dota_constants import EVENT_NAME_MAPPING

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
"""

event_values = {
    "creep_death": (0.5, 30, 30),
    "creep_to_hero_damage": (0.2, 30, 30),
    "hero_death": (60, 150, 120),
    "hero_to_creep_damage": (0.4, 30, 30),
    "hero_to_hero_damage": (2, 60, 60),
    "hero_to_neutral_damage": (1.2, 30, 30),
    "hero_to_roshan_damage": (2, 60, 60),
    "hero_to_tower_damage": (4, 60, 60),
    "modifier_arcane": (0, 0, 0),
    "modifier_burn": (0, 0, 0),
    "modifier_double_damage": (0, 0, 0),
    "modifier_haste": (0, 0, 0),
    "modifier_invis": (0, 0, 0),
    "modifier_invis_reveal": (0, 0, 0),
    "modifier_invulnerable": (0, 0, 0),
    "modifier_magic_immune": (0, 0, 0),
    "modifier_regen": (0, 0, 0),
    "modifier_root": (0, 0, 0),
    "modifier_silence": (0, 0, 0),
    "modifier_slow": (0, 0, 0),
    "modifier_smoke": (5, 60, 60),
    "modifier_stun": (0, 0, 0),
    "neutral_death": (3, 60, 60),
    "neutral_to_hero_damage": (0.7, 30, 30),
    "roshan_death": (75, 150, 120),
    "roshan_to_hero_damage": (2, 60, 60),
    "tower_death": (60, 120, 90),
    "tower_to_hero_damage": (1.5, 60, 60)

}

tick_interval = 15

def get_event_values(tick):
    res = [0] * 33

    for event in events:
        if (tick < event.min_tick) or (tick > event.max_tick): continue
        val_dict = event.get_future_values(tick, tick_interval)

        for k in val_dict:
            res[k] += val_dict[k]

    # softmax function
    res = np.exp(res)
    res = list(res / np.sum(res))

    # max target and such
    res.extend([np.argmax(res), tick])

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

        # get event value and disregard zero events
        val = event_values[rowd['event']]
        if (val[0] == 0): continue

        name_1 = rowd['primary_target']
        if not pd.isnull(rowd['primary_target_idx']):
            name_1 += "_{}".format(int(rowd['primary_target_idx']))

        name_2 = rowd['secondary_target']
        if not pd.isnull(rowd['secondary_target_idx']):
            name_2 += "_{}".format(int(rowd['secondary_target_idx']))

        events.append(Event(rowd['tick'], val[0], val[1], val[2], name_1, name_2))

    # produce Y values
    print("Ready to calculate!")
    ticks = list(X_df['tick'])
    y = []
    for tick in tqdm(ticks):
        y.append(get_event_values(tick))

    cols = list(EVENT_NAME_MAPPING.keys()) + ['target', 'tick']
    df_y = pd.DataFrame(y, columns=cols)
    df_y.to_csv(sys.argv[3])


