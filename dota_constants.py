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

MODIFIER_MAP = {
    "modifier_stunned": "stun",
    "modifier_earthshaker_fissure_stun": "stun",
    "modifier_tiny_avalanche_stun": "stun",
    "modifier_jakiro_ice_path_stun": "stun",
    "modifier_monkey_king_boundless_strike_stun": "stun",
    "modifier_monkey_king_unperched_stunned": "stun",
    "modifier_techies_stasis_trap_stunned": "stun",
    "modifier_bashed": "stun",
    "modifier_special_bonus_20_bash": "stun",
    "modifier_slardar_bash": "stun",
    "modifier_nian_greater_bash": "stun",
    "modifier_nian_greater_bash_speed": "stun",
    "modifier_roshan_bash": "stun",
    "modifier_lycan_summon_wolves_bash": "stun",
    "modifier_spirit_breaker_greater_bash": "stun",
    "modifier_spirit_breaker_greater_bash_speed": "stun",
    "modifier_item_cranium_basher": "stun",
    "modifier_silence": "silence",
    "modifier_drowranger_wave_of_silence_knockback": "silence",
    "modifier_silencer_curse_of_the_silent": "silence",
    "modifier_silencer_last_word": "silence",
    "modifier_silencer_global_silence": "silence",
    "modifier_disarmed": "disarm",
    "modifier_invoker_deafening_blast_disarm": "disarm",
    "modifier_shredder_chakram_disarm": "disarm",
    "modifier_creep_slow": "slow",
    "modifier_ghost_frost_attack_slow": "slow",
    "modifier_ogre_magi_frost_armor_slow": "slow",
    "modifier_crystal_maiden_freezing_field_slow": "slow",
    "modifier_drow_ranger_frost_arrows_slow": "slow",
    "modifier_kunkka_torrent_slow": "slow",
    "modifier_lich_attack_slow": "slow",
    "modifier_lich_attack_slow_debuff": "slow",
    "modifier_lich_frostnova_slow": "slow",
    "modifier_lich_chainfrost_slow": "slow",
    "modifier_lich_frostarmor_slow": "slow",
    "modifier_razor_unstablecurrent_slow": "slow",
    "modifier_sand_king_caustic_finale_slow": "slow",
    "modifier_sand_king_epicenter_slow": "slow",
    "modifier_skeleton_king_reincarnate_slow": "slow",
    "modifier_storm_spirit_electric_vortex_self_slow": "slow",
    "modifier_windrunner_windrun_slow": "slow",
    "modifier_beastmaster_primal_roar_slow": "slow",
    "modifier_death_prophet_spirit_siphon_slow": "slow",
    "modifier_faceless_void_time_dilation_slow": "slow",
    "modifier_faceless_void_time_walk_slow": "slow",
    "modifier_sniper_shrapnel_slow": "slow",
    "modifier_sniper_headshot_slow": "slow",
    "modifier_templar_assassin_trap_slow": "slow",
    "modifier_viper_poison_attack_slow": "slow",
    "modifier_viper_corrosive_skin_slow": "slow",
    "modifier_viper_viper_strike_slow": "slow",
    "modifier_bounty_hunter_jinada_slow": "slow",
    "modifier_broodmother_spin_web_slowed": "slow",
    "modifier_dark_seer_wall_slow": "slow",
    "modifier_dragon_knight_frost_breath_slow": "slow",
    "modifier_enchantress_untouchable_slow": "slow",
    "modifier_enchantress_enchant_slow": "slow",
    "modifier_gyrocopter_call_down_slow": "slow",
    "modifier_huskar_life_break_slow": "slow",
    "modifier_invoker_ice_wall_slow_aura": "slow",
    "modifier_invoker_ice_wall_slow_debuff": "slow",
    "modifier_jakiro_dual_breath_slow": "slow",
    "modifier_leshrac_lightning_storm_slow": "slow",
    "modifier_shadow_demon_purge_slow": "slow",
    "modifier_centaur_stampede_slow": "slow",
    "modifier_earth_spirit_rolling_boulder_slow": "slow",
    "modifier_magnataur_skewer_slow": "slow",
    "modifier_medusa_stone_gaze_slow": "slow",
    "modifier_monkey_king_spring_slow": "slow",
    "modifier_skywrath_mage_concussive_shot_slow": "slow",
    "modifier_terrorblade_reflection_slow": "slow",
    "modifier_troll_warlord_whirling_axes_slow": "slow",
    "modifier_tusk_walrus_punch_slow": "slow",
    "modifier_tusk_walrus_kick_slow": "slow",
    "modifier_undying_tombstone_zombie_deathstrike_slow": "slow",
    "modifier_undying_tombstone_zombie_deathstrike_slow_counter": "slow",
    "modifier_winter_wyvern_arctic_burn_slow": "slow",
    "modifier_winter_wyvern_splinter_blast_slow": "slow",
    "modifier_wisp_tether_slow": "slow",
    "modifier_item_diffusal_blade_slow": "slow",
    "modifier_item_ethereal_blade_slow": "slow",
    "modifier_item_orb_of_venom_slow": "slow",
    "modifier_item_skadi_slow": "slow",
    "magic_immune": "magic_immune",
    "modifier_magic_immune": "magic_immune",
    "modifier_hexxed": "hex",
    "modifier_doom_bringer_doom": "mute",
    "modifier_rune_doubledamage": "dd",
    "modifier_rune_haste": "haste",
    "modifier_rune_invis": "invis",
    "modifier_persistent_invisibility": "invis",
    "modifier_invisible": "invis",
    "modifier_nevermore_requiem_invis_break": "invis",
    "modifier_sandking_sand_storm_invis": "invis",
    "modifier_windrunner_windrun_invis": "invis",
    "modifier_beastmaster_hawk_invisibility_activator": "invis",
    "modifier_beastmaster_hawk_invisibility": "invis",
    "modifier_riki_permanent_invisibility": "invis",
    "modifier_broodmother_spin_web_invisible_applier": "invis",
    "modifier_lycan_summon_wolves_invisibility": "invis",
    "modifier_treant_natures_guise_invis": "invis",
    "modifier_item_invisibility_edge": "invis",
    "modifier_item_invisibility_edge_windwalk": "invis"
}