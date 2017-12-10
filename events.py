CONST_EPS = 0.0000001
import math

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
        self.pre_lam = -math.log(CONST_EPS/max_value)/ (pre_ticks)
        self.post_lam = -math.log(CONST_EPS/max_value)/ (post_ticks)


    def calculate_value(self, tick, method="decay"):
        def decay(lam, t):
            return self.max_value * math.exp(-lam * t)

        def in_range(tick):
            return tick >= self.tick - self.pre_ticks and tick <= self.tick + self.post_ticks

        if (method == "decay"):
            res =  decay(self.post_lam, tick - self.tick) if tick > self.tick else decay(self.pre_lam, self.tick - tick)
            if (res > CONST_EPS):
                return res
        elif in_range(tick):
            return self.max_value

        return 0

    def get_values(self, tick, method='decay'):
        res = {}
        val = self.calculate_value(tick, method)
        res[self.name_1] = val
        if (self.name_2 != None):
            res[self.name_2] = val/2.0

        return res



if __name__ == '__main__':
    event = Event(10, 10, 5, 5)

    for i in range(-2, 20):
        print(i, event.calculate_value(i, "decay"))

