CONST_EPS = 0.0000001
import math
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
