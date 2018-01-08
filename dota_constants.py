import pandas as pd

TOWER = 'CDOTA_BaseNPC_Tower'
BARRACK = "CDOTA_BaseNPC_Barracks"
SHRINE = "CDOTA_BaseNPC_Healer"
ANCIENT = "CDOTA_BaseNPC_Fort"
ROSHAN = "CDOTA_Unit_Roshan"
HERO = "CDOTA_Unit_Hero"
COURIER = "CDOTA_Unit_Courier"
RADIANT = 2
DIRE = 3

# TOWERS
RADIANT_T4 = 143
DIRE_T4 = 153

TOWER_UNIT_INDEX = {
    134: 0,  # RADIANT_TOP_T1 = 134
    135: 1,  # RADIANT_MID_T1 = 135
    136: 2,  # RADIANT_BOT_T1 = 136
    137: 3,  # RADIANT_TOP_T2 = 137
    138: 4,  # RADIANT_MID_T2 = 138
    139: 5,  # RADIANT_BOT_T2 = 139
    140: 6,  # RADIANT_TOP_T3 = 140
    141: 7,  # RADIANT_MID_T3 = 141
    142: 8,  # RADIANT_BOT_T3 = 142
    143: 9,  # RADIANT_T4 = 143
    144: 11,  # DIRE_TOP_T1 = 144
    145: 12,  # DIRE_MID_T1 = 145
    146: 13,  # DIRE_BOT_T1 = 146
    147: 14,  # DIRE_TOP_T2 = 147
    148: 15,  # DIRE_MID_T2 = 148
    149: 16,  # DIRE_BOT_T2 = 149
    150: 17,  # DIRE_TOP_T3 = 150
    151: 18,  # DIRE_MID_T3 = 151
    152: 19,  # DIRE_BOT_T3 = 152
    153: 20  # DIRE_T4 = 153
}

TOWER_NAME = {
    134: "RADIANT_TOP_T1",
    135: "RADIANT_MID_T1",
    136: "RADIANT_BOT_T1",
    137: "RADIANT_TOP_T2",
    138: "RADIANT_MID_T2",
    139: "RADIANT_BOT_T2",
    140: "RADIANT_TOP_T3",
    141: "RADIANT_MID_T3",
    142: "RADIANT_BOT_T3",
    143: "RADIANT_T4",
    144: "DIRE_TOP_T1",
    145: "DIRE_MID_T1",
    146: "DIRE_BOT_T1",
    147: "DIRE_TOP_T2",
    148: "DIRE_MID_T2",
    149: "DIRE_BOT_T2",
    150: "DIRE_TOP_T3",
    151: "DIRE_MID_T3",
    152: "DIRE_BOT_T3",
    153: "DIRE_T4"
}

# BARRACKS
BARRACK_UNIT_INDEX = {
    158: 0,  # RADIANT_TOP_RACK_1
    161: 1,  # RADIANT_TOP_RACK_2
    159: 2,  # RADIANT_MID_RACK_1
    162: 3,  # RADIANT_MID_RACK_2
    160: 4,  # RADIANT_BOT_RACK_1
    163: 5,  # RADIANT_BOT_RACK_2
    164: 6,  # DIRE_TOP_RACK_1
    167: 7,  # DIRE_TOP_RACK_2
    165: 8,  # DIRE_MID_RACK_1
    168: 9,  # DIRE_MID_RACK_2
    166: 10,  # DIRE_BOT_RACK_1
    169: 11  # DIRE_BOT_RACK_2
}

BARRACK_NAME = {
    158: "RADIANT_TOP_RACK_1",
    161: "RADIANT_TOP_RACK_2",
    159: "RADIANT_MID_RACK_1",
    162: "RADIANT_MID_RACK_2",
    160: "RADIANT_BOT_RACK_1",
    163: "RADIANT_BOT_RACK_2",
    164: "DIRE_TOP_RACK_1",
    167: "DIRE_TOP_RACK_2",
    165: "DIRE_MID_RACK_1",
    168: "DIRE_MID_RACK_2",
    166: "DIRE_BOT_RACK_1",
    169: "DIRE_BOT_RACK_2"
}

BARRACK_COMBAT_NAME = {
    "npc_dota_goodguys_melee_rax_top": 0,
    "npc_dota_goodguys_melee_rax_mid": 2,
    "npc_dota_goodguys_melee_rax_bot": 4,
    "npc_dota_goodguys_range_rax_top": 1,
    "npc_dota_goodguys_range_rax_mid": 3,
    "npc_dota_goodguys_range_rax_bot": 5,
    "npc_dota_badguys_melee_rax_top": 6,
    "npc_dota_badguys_melee_rax_mid": 8,
    "npc_dota_badguys_melee_rax_bot": 10,
    "npc_dota_badguys_range_rax_top": 7,
    "npc_dota_badguys_range_rax_mid": 9,
    "npc_dota_badguys_range_rax_bot": 11
}

TOWER_COMBAT_NAME = {
    "npc_dota_goodguys_tower1_top": 0, # "RADIANT_TOP_T1"
    "npc_dota_goodguys_tower1_mid": 1, # "RADIANT_MID_T1"
    "npc_dota_goodguys_tower1_bot": 2, # "RADIANT_BOT_T1"
    "npc_dota_goodguys_tower2_top": 3, # "RADIANT_TOP_T2"
    "npc_dota_goodguys_tower2_mid": 4, # "RADIANT_MID_T2"
    "npc_dota_goodguys_tower2_bot": 5, # "RADIANT_BOT_T2"
    "npc_dota_goodguys_tower3_top": 6, # "RADIANT_TOP_T3"
    "npc_dota_goodguys_tower3_mid": 7, # "RADIANT_MID_T3"
    "npc_dota_goodguys_tower3_bot": 8, # "RADIANT_BOT_T3"
    "npc_dota_goodguys_tower4": 9, # "RADIANT_T4"
    "npc_dota_badguys_tower1_top": 11, # "DIRE_TOP_T1"
    "npc_dota_badguys_tower1_mid": 12, # "DIRE_MID_T1"
    "npc_dota_badguys_tower1_bot": 13, # "DIRE_BOT_T1"
    "npc_dota_badguys_tower2_top": 14, # "DIRE_TOP_T2"
    "npc_dota_badguys_tower2_mid": 15, # "DIRE_MID_T2"
    "npc_dota_badguys_tower2_bot": 16, # "DIRE_BOT_T2"
    "npc_dota_badguys_tower3_top": 17, # "DIRE_TOP_T3"
    "npc_dota_badguys_tower3_mid": 18, # "DIRE_MID_T3"
    "npc_dota_badguys_tower3_bot": 19, # "DIRE_BOT_T3"
    "npc_dota_badguys_tower4": 20 # "DIRE_T4
}

ANCIENT_COMBAT_NAME= {
    "npc_dota_goodguys_fort": 0,
    "npc_dota_badguys_fort": 1
}

SHRINE_NAME = {
    155: "RADIANT_SHRINE",
    157: "DIRE_SHRINE"
}


# ANCIENT
RADIANT_ANCIENT = 170
DIRE_ANCIENT = 171

# Shrines
RADIANT_SHRINE = 155
DIRE_SHRINE = 157

_modifiers = pd.read_csv('resources/modifiers.csv')
MODIFIER_MAP = {
    _modifiers.loc[i, 'modifier_name']: _modifiers.loc[i, 'effect']
                           for i in range(len(_modifiers))
}

_class_combat = pd.read_csv('resources/class_combat_mapping.csv')

CLASS_TO_COMBAT_MAPPING = {_class_combat.loc[i, 'class_name']: _class_combat.loc[i, 'combat_name']
                           for i in range(len(_class_combat))}


TEAM_MAPPING = {
    0: "self",
    2: "radiant",
    3: "dire",
    4: "neutral"
}

EVENT_NAME_MAPPING = {
    "hero_0": 0,
    "hero_1": 1,
    "hero_2": 2,
    "hero_3": 3,
    "hero_4": 4,
    "hero_5": 5,
    "hero_6": 6,
    "hero_7": 7,
    "hero_8": 8,
    "hero_9": 9,
    "roshan": 10,
    "tower_0": 11,
    "tower_1": 12,
    "tower_2": 13,
    "tower_3": 14,
    "tower_4": 15,
    "tower_5": 16,
    "tower_6": 17,
    "tower_7": 18,
    "tower_8": 19,
    "tower_9": 20,
    "tower_10": 21,
    "tower_11": 22,
    "tower_12": 23,
    "tower_13": 24,
    "tower_14": 25,
    "tower_15": 26,
    "tower_16": 27,
    "tower_17": 28,
    "tower_18": 29,
    "tower_19": 30,
    "tower_20": 31,
    "tower_21": 32
}