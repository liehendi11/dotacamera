import math

import pandas as pd
from tqdm import tqdm

from events import Event
import sys
import numpy as np

from dota_constants import EVENT_NAME_MAPPING

class EventParser:
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
        "modifier_blind": (0, 0, 0),
        "neutral_death": (3, 60, 60),
        "neutral_to_hero_damage": (0.7, 30, 30),
        "roshan_death": (75, 150, 120),
        "roshan_to_hero_damage": (2, 60, 60),
        "tower_death": (60, 120, 90),
        "tower_to_hero_damage": (1.5, 60, 60)

    }

    def __init__(self, ticks, events, tick_interval):
        self.ticks = ticks
        self.parsed_events_df = events
        self.tick_interval = tick_interval

        self.events = []


    def get_event_values(self, tick):
        res = [0] * 33

        for event in self.events:
            if (tick < event.min_tick) or (tick > event.max_tick): continue
            val_dict = event.get_future_values(tick, self.tick_interval)

            for k in val_dict:
                res[k] += val_dict[k]

        # softmax function
        res = np.exp(res)
        res = list(res / np.sum(res))

        # max target and such
        res.extend([np.argmax(res), tick])

        return res


    def run(self):
        # parse events
        events = []
        for i, row in tqdm(self.parsed_events_df.iterrows()):
            rowd = dict(row)

            # get event value and disregard zero events
            val = self.event_values[rowd['event']]
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
        y = []
        for tick in tqdm(self.ticks):
            y.append(self.get_event_values(tick))

        cols = list(EVENT_NAME_MAPPING.keys()) + ['target', 'tick']
        df_y = pd.DataFrame(y, columns=cols)

        return df_y

