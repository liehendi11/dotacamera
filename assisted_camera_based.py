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

run_debug = False

def select_hero(hero, tick):
    global assisted_cam_toggled, hero_keys, last_key, last_tick

    if 'hero' not in hero:
        return

    if not assisted_cam_toggled:
        if not run_debug: keyboard.press('/')
        assisted_cam_toggled = True

    key = hero_keys[hero]
    if (last_key != key and last_tick < tick) or (last_key == key and last_tick < tick):
        if not run_debug:
            keyboard.press_and_release(key)
            keyboard.press_and_release(key)
        last_key = key
        last_tick = tick


if __name__ == "__main__":
    df = pd.read_csv('test_visual_Y.csv')

    tick_interval = 15
    delay = (1.0 / 30) * tick_interval

    previous_choice = ""
    previous_choice_tick = 0
    smoothing_ratio = 0.3
    smoothing_tick = 4 * 30
    target_swap_ratio = 1.1

    starting_tick = 32000

    for i, row in df.iterrows():
        if row['tick'] < starting_tick:
            continue

        if 'hero' in row['target']:
            print(row['tick'], row['target'], row['secondary_target'], previous_choice)

            previous_choice = str(previous_choice)
            prev_target_ratio = 0.0
            if len(previous_choice) > 0:
                prev_target_ratio = row[previous_choice] / row[row['target']]
            # smoothing
            choice = previous_choice
            if previous_choice != row['target']:  # changing hero to follow
                if (previous_choice_tick + smoothing_tick <= row['tick']) and \
                        prev_target_ratio <= smoothing_ratio:  # it is time to change or a big event is happening
                    choice = row['target']
                    previous_choice_tick = row['tick']
                    previous_choice = row['target']

            elif previous_choice_tick + smoothing_tick > row['tick'] and row[row['target']]/row[row['secondary_target']] < target_swap_ratio:  # similar target, change when it has been more than 4 secs
                choice = row['secondary_target']
                previous_choice_tick = row['tick']
                previous_choice = choice
                print("swap")
            select_hero(choice, row['tick'])

        time.sleep(delay)


