import math

class Entity:
    def __init__(self, name, type, team):
        self.name = name
        self.basic_type = type
        self.basic_alive = True
        self.team = team
        self.position_x = 0
        self.position_y = 0

        self.level = 1

        # health and mana
        self.health = 100
        self.max_health = 100
        self.health_percentage = (float(self.health) * 100.0) / float(self.max_health)

        self.received_damage = []
        self.received_heal = []
        self.dealt_damage = []
        self.dealt_heal = []

    def set_position(self, x=None, y=None):
        self.position_x = x if x else self.position_x
        self.position_y = y if y else self.position_y

    def set_health(self, health=None, max_health = None):
        self.health = health if health else self.health
        self.max_health = max_health if max_health else self.max_health
        self.max_health = max(self.max_health, self.health)
        self.health_percentage = (float(self.health) * 100.0) / float(self.max_health)

    def calculate_distance(self, other_entity):
        x_dist = (self.position_x - other_entity.position_x)**2
        y_dist = (self.position_y - other_entity.position_y) ** 2
        return math.sqrt(x_dist + y_dist)

    def set_level(self, level):
        self.level = level

    def set_died(self):
        self.basic_alive = False

    def set_respawned(self):
        self.basic_alive = True

    def add_received_damage(self, tick, source, damage_value):
        self.received_damage.append((tick, source, int(damage_value)))

    def add_received_heal(self, tick, source, heal_value):
        self.received_heal.append((tick, source, int(heal_value)))

    def add_dealt_damage(self, tick, target, damage_value):
        self.dealt_damage.append((tick, target, int(damage_value)))

    def add_dealt_heal(self, tick, target, heal_value):
        self.dealt_heal.append((tick, target, int(heal_value)))

    def calculate_damage_heal_overtime(self, current_tick, tick_interval):
        # damage
        total_received_damage = 0
        total_dealt_damage = 0
        total_received_heal = 0
        total_dealt_heal = 0

        received_damage_details = {
            "hero_0": 0,
            "hero_1": 0,
            "hero_2": 0,
            "hero_3": 0,
            "hero_4": 0,
            "hero_5": 0,
            "hero_6": 0,
            "hero_7": 0,
            "hero_8": 0,
            "hero_9": 0,
            "creep": 0,
            "building": 0,
            "neutral": 0,
            "roshan": 0
        }
        dealt_damage_details = received_damage_details.copy()
        received_heal_details = received_damage_details.copy()
        dealt_heal_details = received_damage_details.copy()

        for damage in reversed(self.received_damage):
            if damage[0] >= (current_tick - tick_interval + 1):
                total_received_damage += damage[2]
                received_damage_details[damage[1]] += damage[2]
            else:
                break


        for damage in reversed(self.dealt_damage):
            if damage[0] >= (current_tick - tick_interval + 1):
                total_dealt_damage += damage[2]
                dealt_damage_details[damage[1]] += damage[2]
            else:
                break

        for heal in reversed(self.received_heal):
            if heal[0] >= (current_tick - tick_interval + 1):
                total_received_heal += heal[2]
                received_heal_details[heal[1]] += heal[2]
            else:
                break

        for heal in reversed(self.dealt_heal):
            if heal[0] >= (current_tick - tick_interval + 1):
                total_dealt_heal += heal[2]
                dealt_heal_details[heal[1]] += heal[2]
            else:
                break

        res = {
            "total_received_damage": total_received_damage,
            "received_damage": received_damage_details,
            "total_dealt_damage": total_dealt_damage,
            "dealt_damage": dealt_damage_details,
            "total_received_heal": total_received_heal,
            "received_heal": received_heal_details,
            "total_dealt_heal": total_dealt_heal,
            "dealt_heal": dealt_heal_details,
        }
        return res

class Roshan(Entity):
    def __init__(self):
        Entity.__init__(self, "roshan", "roshan", "neutral")

class Tower(Entity):
    def __init__(self, name, team):
        Entity.__init__(self, name, "tower", team)

class Shrine(Entity):
    def __init__(self, name, team):
        Entity.__init__(self, name, "shrine", team)

class Courier(Entity):
    def __init__(self, name, team):
        Entity.__init__(self, name, "courier", team)

class Barrack(Entity):
    def __init__(self, name, team):
        Entity.__init__(self, name, "barrack", team)

class Ancient(Entity):
    def __init__(self, team):
        Entity.__init__(self, "ancient", "ancient", team)


class Hero(Entity):
    def __init__(self, name, type, team):
        Entity.__init__(self, name, type, team)

        self.mana = 100
        self.max_mana = 100
        self.mana_percentage = (float(self.mana) * 100.0) / float(self.max_mana)

        # modifiers_stack
        self.modifiers_stack = {
            "slow": 0,
            "stun": 0,
            "burn": 0,
            "invis": 0,
            "regen": 0,
            "root": 0,
            "invulnerable": 0,
            "silence": 0,
            "disarm": 0,
            "invis_reveal": 0,
            "haste": 0,
            "blind": 0,
            "magic_immune": 0,
            "break": 0,
            "mute": 0,
            "hex": 0,
            "arcane": 0,
            "smoke": 0,
            "double_damage": 0
        }

        # resource and actions
        self.stats = {
            "networth": 0,
            "gpm": 0,
            "xpm": 0,
            "kills": 0,
            "deaths": 0,
            "assists": 0,
            "last_hits": 0,
            "denies": 0,
            "kill_streak":0
        }

    def set_mana(self, mana=None, max_mana=None):
        self.mana = mana if mana else self.mana
        self.max_mana = max_mana if max_mana else self.max_mana
        self.max_mana = max(self.max_mana, self.mana)
        self.mana_percentage = (float(self.mana) * 100.0) / float(self.max_mana)

    def add_modifier(self, type):
        self.modifiers_stack[type] += 1

    def remove_modifier(self, type):
        self.modifiers_stack[type] -= 1

    def set_stats(self, stat, value):
        self.stats[stat] = value

    def set_died(self):
        # death is the strongest purge
        for k in self.modifiers_stack:
            self.modifiers_stack[k] = False

        self.basic_alive = False






