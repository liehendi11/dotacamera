import keyboard
import pandas as pd
import numpy as np
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

#assisted_cam_toggled = False
last_key = ""
last_tick = 0

run_debug = False

def select_hero(hero, tick):
    # global assisted_cam_toggled,
    global hero_keys, last_key, last_tick

    if 'hero' not in hero:
        return

    # if not assisted_cam_toggled:
    #     if not run_debug: keyboard.press('F11')
    #     assisted_cam_toggled = True

    key = hero_keys[hero]
    if (last_key != key and last_tick < tick) or (last_key == key and last_tick < tick):
        if not run_debug:
            keyboard.press_and_release(key)
            keyboard.press_and_release(key)
        last_key = key
        last_tick = tick

def checkEqual(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)

if __name__ == "__main__":
    #df = pd.read_csv('test_visual_Y.csv')
    df = pd.read_csv('letor_y/3554472677_y.txt', sep='\t', header=None)

    tick_interval = 15
    delay = (1.0 / 30) * tick_interval

    previous_choice = ""
    previous_choice_tick = 0
    smoothing_ratio = 0.3
    smoothing_tick = 4 * 30
    min_swap_tick = 1 * 30
    target_swap_ratio = 1.1
    speed_check = time.time()
    choice = ""

    starting_tick = 52500


    # Letor Dataset
    tick_list = df.iloc[:,0].unique()
    for i in range(len(tick_list)):
        start = time.time()
        if tick_list[i] < starting_tick:
            continue
        tick_data = df[df.iloc[:,0] == tick_list[i]].sort_values(2, ascending=False)

        is_pregame = checkEqual(tick_data.iloc[:,2])

        print(is_pregame, tick_list[i], tick_data.iloc[0,1], tick_data.iloc[1,1])

        if len(previous_choice) > 0:
            previous_choice = str(previous_choice)

        if (is_pregame):
            if (tick_list[i] >= previous_choice_tick + smoothing_tick):
                if (len(previous_choice) == 0):
                    # print('pre-game init')
                    previous_choice_tick = tick_list[i]
                    previous_choice = str(tick_data.iloc[0,1])
                else:
                    # print('pre-game swap 4s')
                    previous_choice_tick = tick_list[i]
                    if ((int(previous_choice) + 5) > 9):
                        previous_choice = (int(previous_choice) + 6) % 5
                    else:
                        previous_choice = int(previous_choice) + 5
                    previous_choice = str(previous_choice)
        else:
            # smoothing
            if ((len(previous_choice) == 0) or (tick_list[i] >= previous_choice_tick + smoothing_tick)):
                # print('swap 4s')
                previous_choice_tick = tick_list[i]
                previous_choice = str(tick_data.iloc[0,1])
            elif (tick_list[i] >= previous_choice_tick + min_swap_tick):
                if ((previous_choice != str(tick_data.iloc[0,1]) and tick_data.iloc[0,1] > tick_data.iloc[int(previous_choice),1])):
                    # print('swap min')
                    previous_choice_tick = tick_list[i]
                    # update prev choice on event
                    previous_choice = str(tick_data.iloc[0,1])
                else:
                    print('smooth')
        select_hero('hero_'+ str(previous_choice), tick_list[i])
        end = time.time()
        # print('timer: '+ str(end-start))

    # Non-Letor

    # for i, row in df.iterrows():
    #     if row['tick'] < starting_tick:
    #         continue
    #
    #     if 'hero' in row['target']:
    #         print(row['tick'], row['target'], row['secondary_target'], previous_choice)
    #
    #         previous_choice = str(previous_choice)
    #         prev_target_ratio = 0.0
    #         if len(previous_choice) > 0:
    #             prev_target_ratio = row[previous_choice] / row[row['target']]
    #         # smoothing
    #         choice = previous_choice
    #         if previous_choice != row['target']:  # changing hero to follow
    #             if (previous_choice_tick + smoothing_tick <= row['tick']) and \
    #                     prev_target_ratio <= smoothing_ratio:  # it is time to change or a big event is happening
    #                 choice = row['target']
    #                 previous_choice_tick = row['tick']
    #                 previous_choice = row['target']
    #
    #         elif previous_choice_tick + smoothing_tick > row['tick'] and row[row['target']]/row[row['secondary_target']] < target_swap_ratio:  # similar target, change when it has been more than 4 secs
    #             choice = row['secondary_target']
    #             previous_choice_tick = row['tick']
    #             previous_choice = choice
    #             print("swap")
    #         select_hero(choice, row['tick'])
        print(str((end-start)) + '- | -'+ str(speed_check - end))
        time.sleep(delay- (end-start))


