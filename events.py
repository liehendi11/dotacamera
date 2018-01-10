CONST_EPS = 0.0000001
import math

import numpy as np
import pandas as pd
from tqdm import tqdm

from dota_constants import EVENT_NAME_MAPPING

class Event:
    def __init__(self, tick, max_value, pre_ticks, post_ticks, name_1, name_2):
        self.tick = tick
        self.max_value = max_value
        self.pre_ticks = pre_ticks
        self.post_ticks = post_ticks
        self.max_tick = tick + post_ticks
        self.min_tick = tick - pre_ticks
        self.name_1 = name_1
        self.name_2 = name_2

        # compute constants
        light = 2
        offset_size = 0.1
        self.pre_offset = pre_ticks * offset_size
        self.post_offset = post_ticks * offset_size
        self.pre_lam = -math.log(CONST_EPS/max_value)/ ((pre_ticks * 0.8) * light)
        self.post_lam = -math.log(CONST_EPS/max_value)/ ((post_ticks * 0.8) * light)


    def calculate_value(self, tick, method="decay"):
        def decay(lam, t):
            return self.max_value * math.exp(-lam * t)

        def in_range(tick):
            return tick >= self.tick - self.pre_ticks and tick <= self.tick + self.post_ticks

        if (method == "decay"):
            if ((tick >= self.tick - self.pre_offset) and (tick <= self.tick + self.post_offset)):
                res = self.max_value
            else:
                res =  decay(self.post_lam, tick - self.tick) if tick > self.tick else decay(self.pre_lam, self.tick - tick)

            if (res > CONST_EPS):
                return res
        elif in_range(tick):
            return self.max_value

        return 0

    def get_values(self, tick, method='decay'):
        res = [0, 0]

        # res = {}
        val = self.calculate_value(tick, method)
        res[0] = val
        if isinstance(self.name_2, str) and (not self.name_2 in ('creep', 'neutral')):
            res[1] = val/2.0

        return res

    def get_future_values(self, tick, tick_interval, method='decay'):
        res = {}
        for i in range(tick, tick+tick_interval):
            t_res = self.get_values(i, method)

            res[EVENT_NAME_MAPPING[self.name_1]] = t_res[0]
            if isinstance(self.name_2, str) and (not self.name_2 in ('creep', 'neutral')):
                res[EVENT_NAME_MAPPING[self.name_2]] = t_res[1]

        return res

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
        "modifier_disarm": (0, 0, 0),
        "modifier_burn": (0, 0, 0),
        "modifier_mute": (0, 0, 0),
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
        "modifier_break": (0, 0, 0),
        "modifier_hex": (0, 0, 0),
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
        # res = np.exp(res)
        # res = list(res / np.sum(res))

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


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    hero_kill = Event(200, 60, 150, 120, 0, 0)
    tower_kill = Event(230, 40, 120, 120, 0, 0)

    hero_kill_vals = [hero_kill.calculate_value(i, "decay") for i in range(50, 330, 5)]
    neutral_kill_vals = [tower_kill.calculate_value(i, "decay") for i in range(50, 330, 5)]


    plt.plot(hero_kill_vals, c='r')
    plt.plot(neutral_kill_vals, c='b')

    plt.show()
    exit(0)
