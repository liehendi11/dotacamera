import pandas as pd
import numpy as np
import sys
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler
import os.path
import re
import requests

LIVE_COMBAT_LOG_PATH = 'C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/'
#LIVE_COMBAT_LOG_PATH = 'D:/Project/Dota 2 Automated Camera/python/dotacamera'

PARSED_COMBAT_LOG_PATH = "./parsed_combat_log.csv"
COMBAT_LOG_COLS = ['tick', 'event', 'source', 'is_source_illu', 'source_team', 'target', 'is_target_illu', 'inflictor',
                   'value', 'before', 'after', 'dmg_source']

def parse_combat_type(combat_type):
    return {
        0: 'damage',
        1: 'heal',
        2: 'modifier_add',
        3: 'modifier_remove',
        4: 'death',
        5: 'ability_cast',
        6: 'item',
        7: 'location',
        8: 'gold',
        9: 'game_state',
        10: 'xp',
        11: 'purchase',
        12: 'buyback',
        13: 'ability_trigger',
        14: 'playerstats_value',
        15: 'multikill',
        16: 'killstreak',
        17: 'team_building_kill',
        18: 'first_blood',
        19: 'modifier_refresh',
        20: 'neutral_camp_stack',
        21: 'pickup_rune',
        22: 'revealed_invisible',
        23: 'hero_saved',
        24: 'mana_restored',
        25: 'hero_levelup',
        26: 'bottle_heal_ally',
        27: 'endgame_stats',
        28: 'interrupt_channel',
        29: 'allied_gold',
        30: 'aegis_taken',
        31: 'mana_damage',
        32: 'physical_damage_prevented',
        33: 'unit_summoned',
        34: 'attack_evade',
        35: 'tree_cut',
        36: 'successful_scan',
        37: 'end_killstreak',
        38: 'bloodstone_charge',
        39: 'critical_damage',
        40: 'spell_absorb'
    }.get(combat_type, '')


def handle_dirty_json(dirty_json):
    '''
    :param dirty_json: JSON string without quotes, comma, and using tab (\t) instead of (\n)
    :return: clean_json
    '''
    clean_json = ''
    # dirty_json = dirty_json.split('\t')
    dirty_json = re.split('\t| \n', dirty_json)
    # print(dirty_json)
    count = 0
    for x in dirty_json:
        if not x.isspace() or x != '':
            # print('x = '+x)
            if '{' in x and count == 0:
                clean_json = clean_json + '{'

            else:
                splitted_x = x.split(': ')
                data_key = splitted_x[0]
                # handle double value in JSON
                if data_key == 'value' and clean_json.count('value') % 2 == 1:
                    data_key = 'after_value'

                data_val = splitted_x[1]
                end_json = ''
                if data_val.endswith('}') or x == dirty_json[-1]:
                    end_json = '\n}'
                    data_val = data_val.rstrip('}')
                    data_val = data_val.rstrip('\n')
                elif '{' in x and count > 0 and x != dirty_json[-1]:
                    end_json = '\n},\n{'
                    count = 0
                    data_val = data_val.rstrip('\n},\n{')
                else:
                    end_json = ''

                data_val = data_val.rstrip('\n')
                try:
                    float(data_val)
                except ValueError:
                    data_val = '"' + data_val + '"'
                if clean_json == '{' or count == 1:
                    clean_json = clean_json + '\n' + '"' + data_key + '": ' + data_val + end_json
                else:
                    clean_json = clean_json + ',\n' + '"' + data_key + '": ' + data_val + end_json

            count = count +1
    return '[' + clean_json + ']'


class ChangeHandler(FileSystemEventHandler):

    is_updating = False
    is_appending_log = False

    print('test')
    if os.path.exists(LIVE_COMBAT_LOG_PATH + 'combatlog_out.txt'):
        file = open(LIVE_COMBAT_LOG_PATH + 'combatlog_out.txt', 'r')
        prev_data = file.read()

        file.close()
    else:
        prev_data = ''
    print('prev data '+prev_data)

    def process_update(self, updates, create_new):
        if not self.is_updating:
            is_updating = True
            updates = handle_dirty_json(updates)
            json_all_data = json.loads(updates, strict=False)
            new_combat_log = []
            '''
            Note: 
            Combat log data
            tick, event (game_state/gold/modifier_add/purchase/damage/etc), source, is_source_illu, source_team, target, is_target_illu, 
            inflictor, value, before, after, dmg_source
            '''
            for json_data in json_all_data:
                if not self.is_appending_log:
                    print(json.dumps(json_data, indent=2))
                    self.is_appending_log=True
                    combat_type = parse_combat_type(json_data['type'])

                    #new_log = []
                    # count value before event
                    value_before = ''
                    if combat_type == 'heal' or combat_type == 'mana_restored' or combat_type == 'bottle_heal_ally':
                        value_before = json_data.get('value', 0) - json_data.get('after_value', 0)
                    elif combat_type == 'damage' or combat_type == 'mana_damage' or combat_type == 'critical_damage':
                        value_before = json_data.get('value', 0) + json_data.get('after_value', 0)
                    '''
                    new_log.append({
                        'tick': json_data.get('timestamp', ''),
                        'event': combat_type,
                        'source': json_data.get('attacker_name', ''),
                        'is_source_illu': json_data.get('is_attacker_illusion', ''),
                        'source_team': json_data.get('source_team', ''),
                        'target': json_data.get('target', ''),
                        'is_target_illu': json_data.get('is_target_illusion', ''),
                        'inflictor': json_data.get('inflictor', ''),
                        'value': json_data.get('value', ''),
                        'before': value_before,
                        'after': json_data.get('after_value', ''),
                        'dmg_source': json_data.get('damage_source', '')
                    })
                    '''
                    new_log = pd.Series([json_data.get('timestamp', ''),
                        combat_type,
                        json_data.get('attacker_name', ''),
                        json_data.get('is_attacker_illusion', ''),
                        json_data.get('source_team', ''),
                        json_data.get('target', ''),
                        json_data.get('is_target_illusion', ''),
                        json_data.get('inflictor', ''),
                        json_data.get('value', ''),
                        value_before,
                        json_data.get('after_value', ''),
                        json_data.get('damage_source', '')], index=COMBAT_LOG_COLS)
                    new_combat_log.append(new_log)
                    self.is_appending_log=False
            # parsed_combat_log.append(new_log, ignore_index=True)
            try:
                parsed_combat_log = pd.read_csv(PARSED_COMBAT_LOG_PATH)
                if create_new == 1:
                    parsed_combat_log.empty()
                    parsed_combat_log.to_csv(PARSED_COMBAT_LOG_PATH)
            except FileNotFoundError:
                parsed_combat_log = pd.DataFrame()
            new_combat_log_df = pd.DataFrame(new_combat_log,columns=COMBAT_LOG_COLS)
            print(new_combat_log_df)
            parsed_combat_log = parsed_combat_log.append(new_combat_log,ignore_index=True)

            # filter only data related to heroes
            new_combat_log_filtered = new_combat_log_df[(new_combat_log_df['source'].str.contains('hero')) |
                                                       (new_combat_log_df['target'].str.contains('hero')) |
                                                       (new_combat_log_df['dmg_source'].str.contains('hero'))]
            parsed_combat_log_json = new_combat_log_filtered.to_json(orient='records')

            requests.post('http://127.0.0.1:12345/dota2_live_combat_log', json=parsed_combat_log_json)

            parsed_combat_log.to_csv(PARSED_COMBAT_LOG_PATH,index=False)
            self.is_updating = False

    def on_modified(self, event):
        if 'combatlog_out' in event.src_path:
            print('update found')
            file = open(event.src_path, 'r')
            new_data = file.read()

            # get update and process
            updates = new_data.replace(self.prev_data, "")
            if updates.rstrip() != "":
                self.process_update(updates, 0)
            else:
                print('do nothing')

            # update prev_data
            self.prev_data = new_data
            file.close()

    def on_created(self, event):
        if 'combatlog_out' in event.src_path:
            file = open(event.src_path, 'r')

            # init prev_data
            self.prev_data = file.read()
            file.close()

            # process initial data
            self.process_update(self.prev_data, 1)


if __name__ == '__main__':
    '''
    Run this with "python live_combatlog_parser.py [2]"
    Output files: (LATER)
    1. Parsed combat log
    '''

    if len(sys.argv) != 1:
        print("Wrong parameters supplied. Exiting...")
        exit(1)

    # read files

    observer = Observer()
    observer.schedule(ChangeHandler(), path=LIVE_COMBAT_LOG_PATH, recursive=False)
    observer.start()

    try:
        while True:
            # print('waiting for update on '+ LIVE_COMBAT_LOG_PATH)
            # check update on combat log every tick (i.e. 1/30 sec)
            time.sleep(1/60)

    except KeyboardInterrupt:
        observer.stop()
        print('interrupted')

    observer.join()

    # combat log
