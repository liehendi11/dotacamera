from collections import deque
from itertools import chain

import pandas as pd
from tqdm import tqdm

from dota_constants import *
from entities import *

'''
3 files required
1. game info -> game starting ticks, entities team and names // done
2. combat log -> damage, heal, modifier, xp, gold, game_state
3. entity change -> all sort of property changes

'''

used_unit_indexes = set()

heroes = [None] * 10  #type: List[Hero]
couriers = []  #type: List[Courier]

towers = [None] * 22  #type: List[Tower]
tower_indexes = {}

barracks = [None] * 12  #type: List[Barrack]
shrines = [None] * 4  #type: List[Shrine]
ancients = [None] * 2  #type: List[Ancient]

roshan = None  #type: Roshan
index_to_array = {}
combat_log_name_to_array = {}

radiant_buildings_name = []
dire_buildings_name = []


starting_tick = 0
ending_tick = 0

logs = []

events = []

def load_basic_info(lifestate):
    global starting_tick, roshan, index_to_array, barracks, shrines, ancients, heroes, couriers, towers, tower_indexes, used_unit_indexes
    for i, row in lifestate.iterrows():
        # add to log queue
        rowd = dict(row)
        logs.append((rowd['tick'], 'lifestate', rowd))

        if (row['action'] == 'death'):
            continue

        if (row['class'] == TOWER):  # towers
            unit_player_index = row['unit_player_index']
            p = TOWER_UNIT_INDEX[unit_player_index]
            j = 0
            name_suffix = ""

            if unit_player_index in (RADIANT_T4, DIRE_T4): # special case, as unit index for both rad and dire t4 are same
                j = 1 if unit_player_index in used_unit_indexes else 0
                name_suffix = "_{}".format(j+1)

            if (not towers[p + j]):  # create a new tower
                towers[p+j] = Tower(TOWER_NAME[unit_player_index] + name_suffix, row['team_num'])
                towers[p+j].set_position(row['x'], row['y'])
                towers[p+j].set_health(row['health'], row['max_health'])
                index_to_array[row['index']] = p + j


            # document used unit indexes to ensure no duplicate towers
            used_unit_indexes.add(unit_player_index)

        if (row['class'] == BARRACK):  # barracks
            unit_player_index = row['unit_player_index']
            p = BARRACK_UNIT_INDEX[unit_player_index]

            if (not barracks[p]):
                barracks[p] = Barrack(BARRACK_NAME[unit_player_index], row['team_num'])
                barracks[p].set_position(row['x'], row['y'])
                barracks[p].set_health(row['health'], row['max_health'])
                index_to_array[row['index']] = p

            # document used unit indexes to ensure no duplicate barracks
            used_unit_indexes.add(unit_player_index)

        if (row['class'] == ROSHAN):
            if (roshan): continue

            roshan = Roshan()
            roshan.set_position(row['x'], row['y'])
            roshan.set_health(row['health'], row['max_health'])
            index_to_array[row['index']] = 0

        if (row['class'] == ANCIENT):
            p = 0 if row['team_num'] == RADIANT else 1
            ancients[p] = Ancient(row['team_num'])
            ancients[p].set_position(row['x'], row['y'])
            ancients[p].set_health(row['health'], row['max_health'])
            index_to_array[row['index']] = p


        if (row['class'] == SHRINE):
            unit_player_index = row['unit_player_index']
            p = 0 if row['team_num'] == RADIANT else 2
            j = 0 if not shrines[p] else 1
            suffix = "_{}".format(j+1)

            shrines[p+j] = Shrine(SHRINE_NAME[unit_player_index] + suffix, row['team_num'])
            shrines[p+j].set_position(row['x'], row['y'])
            shrines[p+j].set_health(row['health'], row['max_health'])
            index_to_array[row['index']] = p+j


        if (HERO in row['class']):
            player_id = row['unit_player_index']

            if (not heroes[player_id]):
                heroes[player_id] = Hero("hero_{}".format(player_id), row['class'], row['team_num'])
                heroes[player_id].set_position(row['x'], row['y'])
                heroes[player_id].set_health(row['health'], row['max_health'])
                index_to_array[row['index']] = player_id

                hero_name = "npc_dota_hero_{}".format('_'.join(row['class'].split('_')[3:]).lower())
                combat_log_name_to_array[hero_name] = player_id

        if (row['class'] == COURIER):
            if (not row['index'] in index_to_array):
                x = len(couriers)
                index_to_array[row['index']] = x
                new_cour = Courier("courier_{}".format(x), row['team_num'])
                new_cour.set_position(row['x'], row['y'])
                new_cour.set_health(row['health'], row['max_health'])

                couriers.append(new_cour)
                index_to_array[row['index']] = x



def load_combat_log(combat_logs):
    global starting_tick, ending_tick
    for i, row in combat_logs.iterrows():
        rowd = dict(row)
        logs.append((rowd['tick'], 'combat', rowd))

        if ((rowd['event'] == 'game_state') and (rowd['value'] == '4')):
            starting_tick = rowd['tick']

        if ((rowd['event'] == 'game_state') and (rowd['value'] == '6')):
            ending_tick = rowd['tick']

def load_property_log(property_log):
    for i, row in property_log.iterrows():
        rowd = dict(row)
        logs.append((rowd['tick'], 'property', rowd))

'''
Combat log events
damage
modifier_add
modifier_remove
xp
death
gold
item
ability cast
ability toggle on
ability toggle off
game state
'''

def process_combat_damage(log):
    # hero x hero
    if ('hero' in log['source']) and ('hero' in log['target']):
        source_name = log['source'].replace(" (illusion)", "")
        target_name = log['target'].replace(" (illusion)", "")

        source_idx = combat_log_name_to_array[source_name]
        target_idx = combat_log_name_to_array[target_name]

        source_hero = heroes[source_idx]  # type: Hero
        target_hero = heroes[target_idx]  # type: Hero

        source_hero.add_dealt_damage(log['tick'], 'hero_{}'.format(target_idx), log['value'])
        target_hero.add_received_damage(log['tick'], 'hero_{}'.format(source_idx), log['value'])
        events.append((log['tick'], "damage", "hero", target_idx, "hero", source_idx))

    # creep x hero
    if ('creep' in log['source'] and ('hero' in log['target'])):
        target_name = log['target']

        if not target_name in combat_log_name_to_array: return
        target_idx = combat_log_name_to_array[target_name]
        target_hero = heroes[target_idx]  # type: Hero

        target_hero.add_received_damage(log['tick'], 'creep', log['value'])
        events.append((log['tick'], "damage", "hero", target_idx))

    # tower x hero
    if ('tower' in log['source'] and ('hero' in log['target'])):
        target_name = log['target']
        source_name = log['source']

        if not target_name in combat_log_name_to_array: return
        target_idx = combat_log_name_to_array[target_name]
        source_idx = TOWER_COMBAT_NAME[source_name]
        target_hero = heroes[target_idx]  # type: Hero

        target_hero.add_received_damage(log['tick'], 'building', log['value'])

        events.append((log['tick'], "damage", "hero", target_idx, "tower", source_idx))

    # neutral x hero
    if ('neutral' in log['source'] and ('hero' in log['target'])):
        target_name = log['target']

        if not target_name in combat_log_name_to_array: return
        target_idx = combat_log_name_to_array[target_name]
        target_hero = heroes[target_idx]  # type: Hero

        target_hero.add_received_damage(log['tick'], 'neutral', log['value'])
        events.append((log['tick'], "damage", "hero", target_idx, "neutral", None))

    # roshan x hero
    if ('roshan' in log['source'] and ('hero' in log['target'])):
        target_name = log['target']

        if not target_name in combat_log_name_to_array: return
        target_idx = combat_log_name_to_array[target_name]
        target_hero = heroes[target_idx]  # type: Hero

        target_hero.add_received_damage(log['tick'], 'roshan', log['value'])
        events.append((log['tick'], "damage", "roshan", None, "hero", target_idx))

    #########################################3

    # hero x creep
    if ('hero' in log['source'] and ('creep' in log['target'])):
        source_name = log['source'].replace(" (illusion)", "")

        if not source_name in combat_log_name_to_array: return
        source_idx = combat_log_name_to_array[source_name]
        source_hero = heroes[source_idx]  # type: Hero

        source_hero.add_dealt_damage(log['tick'], 'creep', log['value'])
        events.append((log['tick'], "damage", "hero", source_idx, "creep", None))

    # hero x tower
    if ('hero' in log['source'] and ('tower' in log['target'])):
        source_name = log['source'].replace(" (illusion)", "")

        if not source_name in combat_log_name_to_array: return
        source_idx = combat_log_name_to_array[source_name]
        source_hero = heroes[source_idx]  # type: Hero

        source_hero.add_dealt_damage(log['tick'], 'building', log['value'])
        events.append((log['tick'], "damage", "hero", source_idx, "tower", None))

    # hero x neutral
    if ('hero' in log['source'] and ('neutral' in log['target'])):
        source_name = log['source'].replace(" (illusion)", "")

        if not source_name in combat_log_name_to_array: return
        source_idx = combat_log_name_to_array[source_name]
        source_hero = heroes[source_idx]  # type: Hero

        source_hero.add_dealt_damage(log['tick'], 'neutral', log['value'])
        events.append((log['tick'], "damage", "hero", source_idx, "neutral", None))

    # hero x roshan
    if ('hero' in log['source'] and ('roshan' in log['target'])):
        source_name = log['source'].replace(" (illusion)", "")

        if not source_name in combat_log_name_to_array: return
        source_idx = combat_log_name_to_array[source_name]
        source_hero = heroes[source_idx]  # type: Hero

        source_hero.add_dealt_damage(log['tick'], 'roshan', log['value'])
        events.append((log['tick'], "damage", "hero", source_idx, "roshan", None))

def process_combat_heal(log):
    # hero x hero
    if ('hero' in log['source']) and ('hero' in log['target']):
        source_name = log['source'].replace(" (illusion)", "")
        target_name = log['target'].replace(" (illusion)", "")

        if not source_name in combat_log_name_to_array: return
        if not target_name in combat_log_name_to_array: return

        source_idx = combat_log_name_to_array[source_name]
        target_idx = combat_log_name_to_array[target_name]

        source_hero = heroes[source_idx]  # type: Hero
        target_hero = heroes[target_idx]  # type: Hero

        source_hero.add_dealt_heal(log['tick'], 'hero_{}'.format(target_idx), log['value'])
        target_hero.add_received_heal(log['tick'], 'hero_{}'.format(source_idx), log['value'])

        events.append((log['tick'], "damage", "hero", target_idx, "hero", source_idx))


def process_combat_modifier(log):
    if ('hero' in log['target']):
        target_name = log['target']
        if not target_name in combat_log_name_to_array: return

        target_idx = combat_log_name_to_array[target_name]
        target_hero = heroes[target_idx]  # type: Hero

        # stun and bashes
        if not log['inflictor'] in MODIFIER_MAP: return

        if log['event'] == 'modifier_add':
            target_hero.add_modifier(MODIFIER_MAP[log['inflictor']])
            events.append((log['tick'], MODIFIER_MAP[log['inflictor']], "hero", target_idx))
        else:
            target_hero.remove_modifier(MODIFIER_MAP[log['inflictor']])
    #########################################

def process_combat_death(log):
    # hero x hero
    if ('hero' in log['source']) and ('hero' in log['target']):
        source_name = log['source'].replace(" (illusion)", "")
        target_name = log['target'].replace(" (illusion)", "")

        source_idx = combat_log_name_to_array[source_name]
        target_idx = combat_log_name_to_array[target_name]

        events.append((log['tick'], "death", "hero", target_idx, "hero", source_idx))

    # creep x hero
    if ('creep' in log['source'] and ('hero' in log['target'])):
        target_name = log['target']

        if not target_name in combat_log_name_to_array: return
        target_idx = combat_log_name_to_array[target_name]

        events.append((log['tick'], "death", "hero", target_idx))

    # tower x hero
    if ('tower' in log['source'] and ('hero' in log['target'])):
        target_name = log['target']
        source_name = log['source']

        if not target_name in combat_log_name_to_array: return
        target_idx = combat_log_name_to_array[target_name]
        source_idx = TOWER_COMBAT_NAME[source_name]

        events.append((log['tick'], "death", "hero", target_idx, "tower", source_idx))

    # neutral x hero
    if ('neutral' in log['source'] and ('hero' in log['target'])):
        target_name = log['target']

        if not target_name in combat_log_name_to_array: return
        target_idx = combat_log_name_to_array[target_name]

        events.append((log['tick'], "death", "hero", target_idx, "neutral", None))

    # roshan x hero
    if ('roshan' in log['source'] and ('hero' in log['target'])):
        target_name = log['target']

        if not target_name in combat_log_name_to_array: return
        target_idx = combat_log_name_to_array[target_name]
        events.append((log['tick'], "death", "hero", target_idx, "roshan", None))

    # hero x creep
    if ('hero' in log['source'] and ('creep' in log['target'])):
        source_name = log['source'].replace(" (illusion)", "")

        if not source_name in combat_log_name_to_array: return
        source_idx = combat_log_name_to_array[source_name]

        events.append((log['tick'], "death", "hero", source_idx, "creep", None))

    # hero x tower
    if ('hero' in log['source'] and ('tower' in log['target'])):
        source_name = log['source'].replace(" (illusion)", "")
        target_name = log['target']

        if not source_name in combat_log_name_to_array: return
        target_idx = TOWER_COMBAT_NAME[target_name]
        source_idx = combat_log_name_to_array[source_name]
        events.append((log['tick'], "death", "tower", target_idx, "hero", source_idx))

    # hero x neutral
    if ('hero' in log['source'] and ('neutral' in log['target'])):
        source_name = log['source'].replace(" (illusion)", "")

        if not source_name in combat_log_name_to_array: return
        source_idx = combat_log_name_to_array[source_name]

        events.append((log['tick'], "death", "hero", source_idx, "neutral", None))

    # hero x roshan
    if ('hero' in log['source'] and ('roshan' in log['target'])):
        source_name = log['source'].replace(" (illusion)", "")

        if not source_name in combat_log_name_to_array: return
        source_idx = combat_log_name_to_array[source_name]
        events.append((log['tick'], "death", "roshan", None, "hero", source_idx))

    return

def process_combat_log(log):
    if log['event'] == 'damage':
        process_combat_damage(log)
    if log['event'] == 'heal':
        process_combat_heal(log)
    if log['event'] == 'death':
        process_combat_death(log)
    return

def process_lifestate_log(log):
    if (log['index'] in index_to_array) or ('Roshan' in log['class']):
        ent = None  # type: Entity

        if ('Roshan' in log['class']):
            ent = roshan
        else:
            idx = index_to_array[log['index']]

        if ('Tower' in log['class']):
            ent = towers[idx]
        if ('Barracks' in log['class']):
            ent = barracks[idx]
        if ('Fort' in log['class']):
            ent = ancients[idx]
        if ('Healer' in log['class']):
            ent = shrines[idx]
        if ('Courier' in log['class']):
            ent = couriers[idx]
        if ('Hero' in log['class']):
            ent = heroes[idx]

        # if (not ent): return 1

        if (log['action'] == 'spawn'):
            ent.set_respawned()
        else:
            ent.set_died()

        return 0
    return 1

def process_property_log(log):
    global ancients, index_to_array, heroes

    if (log['event'] in ('ancient', 'barracks', 'courier', 'roshan', 'tower')):
        ent = None  #type: Entity

        if (log['event'] == 'ancient'):
            ent = ancients[index_to_array[log['index']]]
        if (log['event'] == 'barracks'):
            ent = barracks[index_to_array[log['index']]]
        if (log['event'] == 'courier'):
            ent = couriers[index_to_array[log['index']]]
        if (log['event'] == 'roshan'):
            ent = roshan
        if (log['event'] == 'tower'):
            ent = towers[index_to_array[log['index']]]

        if ('X' in log['property']):
            ent.set_position(x=log['value'])
        if ('Y' in log['property']):
            ent.set_position(y=log['value'])
        if ('iHealth' in log['property']):
            ent.set_health(health=log['value'])
        if ('iMaxHealth' in log['property']):
            ent.set_health(max_health=log['value'])

        return 0

    if ('hero' in log['event']):
        hero = None  #type: Hero
        if ('PlayerResource' in log['class']) or\
                (log['class'] in ('CDOTA_DataDire', 'CDOTA_DataRadiant')):
            idx = int(log['property'].split('.')[1])

            hero = heroes[idx]

            if ('Kills' in log['property']):
                hero.set_stats(stat='kills', value=log['value'])
            if ('Assists' in log['property']):
                hero.set_stats(stat='assists', value=log['value'])
            if ('Deaths' in log['property']):
                hero.set_stats(stat='deaths', value=log['value'])
            if ('Kills' in log['property']):
                hero.set_stats(stat='kills', value=log['value'])
            if ('iNetWorth' in log['property']):
                hero.set_stats(stat='networth', value=log['value'])

        if ('Unit_Hero_' in log['class']):
            if not log['index'] in index_to_array: return 1
            idx = index_to_array[log['index']]
            hero = heroes[idx]

            if ('iHealth' in log['property']):
                hero.set_health(health=log['value'])
            if ('iCurrentLevel' in log['property']):
                hero.set_level(level=log['value'])
            if ('X' in log['property']):
                hero.set_position(x=log['value'])
            if ('Y' in log['property']):
                hero.set_position(y=log['value'])
            if ('flMana' in log['property']):
                hero.set_mana(mana=log['value'])

    return 1

def get_snapshot(tick):
    snapshot = {}

    # hero snapshot
    for i in range(len(heroes)):
        hero = heroes[i]  # type: Hero
        snapshot["hero_{}_alive".format(i)] = hero.basic_alive
        # snapshot["hero_{}_team".format(i)] = hero.team
        snapshot["hero_{}_x".format(i)] = hero.position_x
        snapshot["hero_{}_y".format(i)] = hero.position_y
        snapshot["hero_{}_level".format(i)] = hero.level
        snapshot["hero_{}_health".format(i)] = hero.health
        snapshot["hero_{}_max_health".format(i)] = hero.max_health
        snapshot["hero_{}_health_percentage".format(i)] = hero.health_percentage
        snapshot["hero_{}_mana".format(i)] = hero.mana
        snapshot["hero_{}_max_mana".format(i)] = hero.max_mana
        snapshot["hero_{}_mana_percentage".format(i)] = hero.mana_percentage

        for modifier in hero.modifiers_stack:
            snapshot["hero_{}_{}".format(i, modifier)] = hero.modifiers_stack[modifier] != 0

        for stat in hero.stats:
            snapshot["hero_{}_{}".format(i, stat)] = hero.stats[stat]

    # other entities
    for ent in chain(towers, barracks, shrines, [roshan], ancients, couriers):
        snapshot["{}_{}_alive".format(ent.name, i)] = ent.basic_alive
        snapshot["{}_{}_team".format(ent.name, i)] = ent.team
        snapshot["{}_{}_x".format(ent.name, i)] = ent.position_x
        snapshot["{}_{}_y".format(ent.name, i)] = ent.position_y
        snapshot["{}_{}_level".format(ent.name, i)] = ent.level
        snapshot["{}_{}_health".format(ent.name, i)] = ent.health
        snapshot["{}_{}_max_health".format(ent.name, i)] = ent.max_health
        snapshot["{}_{}_health_percentage".format(ent.name, i)] = ent.health_percentage

    # distances
    # hero to hero
    for i in range(len(heroes)):
        for j in range(i+1, len(heroes)):
            snapshot["dist_hero_{}_hero_{}".format(i,j)] = heroes[i].calculate_distance(heroes[j])

    # hero to entities
    for i in range(len(heroes)):
        hero = heroes[i]  #type: Hero
        for ent in chain(towers, barracks, shrines, [roshan], ancients, couriers):
            snapshot["dist_hero_{}_{}".format(i, ent.name)] = hero.calculate_distance(ent)

    snapshot['tick'] = tick
    return snapshot

def get_interval_snapshot(tick, tick_interval):
    intervals = {}

    for i, hero in enumerate(heroes):
        data = hero.calculate_damage_heal_overtime(tick, tick_interval)

        for j in data:
            if isinstance(data[j], dict):
                for k in data[j]:
                    intervals['{}_hero_{}_{}_{}'.format(tick_interval, i, j, k)] = data[j][k]
            else:
                intervals['{}_hero_{}_{}'.format(tick_interval, i, j)] = data[j]

    return intervals

def start_parsing(tick_interval):
    global logs, ending_tick, starting_tick
    sorted_logs = deque(sorted(logs, key=lambda tup: tup[0]))

    # pre-parsing
    while (len(sorted_logs) > 0) and (sorted_logs[0][0] <= starting_tick):
        tick, log_type, log = sorted_logs.popleft()

        if log_type == 'property':
            process_property_log(log)

        if log_type == 'lifestate':
            process_lifestate_log(log)

    all_snapshots = [{**get_snapshot(tick), **get_interval_snapshot(tick, tick_interval)}]

    for next_tick in tqdm(range(starting_tick + tick_interval, ending_tick+tick_interval, tick_interval)):
        while (len(sorted_logs) > 0) and (sorted_logs[0][0] <= next_tick):
            tick, log_type, log = sorted_logs.popleft()
            if tick > ending_tick:
                all_snapshots.append({**get_snapshot(tick), **get_interval_snapshot(tick, tick_interval)})
                break

            if log_type == 'property':
                process_property_log(log)

            if log_type == 'lifestate':
                process_lifestate_log(log)

            if log_type == 'combat':
                process_combat_log(log)

        all_snapshots.append({**get_snapshot(tick), **get_interval_snapshot(tick, tick_interval)})

    return all_snapshots

if __name__ == '__main__':
    # "tick,action,index,class,unit_player_index,team_num,x,y"
    lifestate_log = pd.read_csv('sample_lifestate_2.csv')
    property_log = pd.read_csv('sample_property_log.csv')
    combat_log = pd.read_csv('sample_combat_log.csv')

    # print(combat_log.info())

    print("Loading files completed")

    # load them
    load_basic_info(lifestate_log)
    load_property_log(property_log)
    load_combat_log(combat_log)

    print("Loading logs to queue completed")

    all_snapshots = start_parsing(12)

    print("Parsing completed")

    df = pd.DataFrame(all_snapshots, columns=all_snapshots[0].keys())
    df.to_csv('sample_X.csv')



    print("Saving X completed")

    df_events = pd.DataFrame(events, columns=['tick', 'event', 'primary_target', 'primary_target_idx',
                                              'secondary_target', 'secondary_target_idx'])
    df_events.to_csv('sample_parsed_events.csv')

    print("Saving Y completed")

