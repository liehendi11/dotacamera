import keyboard
import pandas as pd
import time

hero_keys = {
    "hero_0": "1",
    "hero_1": "2",
    "hero_2": "3",
    "hero_3": "4",
    "hero_4": "5",
    "hero_5": "6",
    "hero_6": "7",
    "hero_7": "8",
    "hero_8": "9",
    "hero_9": "0",
}

assisted_cam_toggled = False
last_key = ""
last_tick = 0

def select_hero(hero, tick):
    global assisted_cam_toggled, hero_keys, last_key, last_tick

    if not assisted_cam_toggled:
        keyboard.press('/')
        assisted_cam_toggled = True

    key = hero_keys[hero]
    if (last_key != key and last_tick < tick) or (last_key == key and last_tick < tick):
        keyboard.press_and_release(key)
        keyboard.press_and_release(key)
        last_key = key
        last_tick = tick


if __name__ == "__main__":
    df = pd.read_csv('test_Y.csv')

    tick_interval = 15
    delay = (1.0 / 30) * tick_interval

    for i, row in df.iterrows():
        if 'hero' in row['target']:
            print(row['tick'], row['target'])
            select_hero(row['target'], row['tick'])

        time.sleep(delay)


