from flask import Flask, request
import sys
import json
import pandas as pd
import live_parser
from live_parser import *
from typing import List

class Hero:
    '''
    def __init__(self, name='', id=0, level, x=0, y=0, hp=0, max_hp=0, health_percent = 0, mana =0, max_mana =0, mana_percent=0,
                 alive=True,silenced=False,stunned=False,disarmed=False,magicimmune=False, hexed=False,muted=False,
                 _break=False,has_debuff=False):
        self.name = name
        self.id = id
        self.level = level
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.alive =alive
    '''
    def __init__(self, json_def, player_index):
        self._is_lifestate_updated = False
        self._is_property_change_updated = False
        self._properties_updated = []
        self._alive = ''
        self._health = 0
        self._max_health = 0
        self._mana = 0
        self._max_mana = 0
        self._level = 0
        self._x = 0
        self._y = 0

        json_dict = json_def
        if player_index < 5:
            self.name = json_dict['hero']['team2'][('player'+str(player_index))]['name']
            self.id = json_dict['hero']['team2'][('player'+str(player_index))]['id']
            self.level = json_dict['hero']['team2'][('player'+str(player_index))]['level']
            self.x = json_dict['hero']['team2'][('player'+str(player_index))]['xpos']
            self.y = json_dict['hero']['team2'][('player'+str(player_index))]['ypos']
            self.health = json_dict['hero']['team2'][('player'+str(player_index))]['health']
            self.max_health = json_dict['hero']['team2'][('player'+str(player_index))]['max_health']
            self.mana = json_dict['hero']['team2'][('player'+str(player_index))]['mana']
            self.max_mana = json_dict['hero']['team2'][('player'+str(player_index))]['max_mana']
            self.alive = json_dict['hero']['team2'][('player'+str(player_index))]['alive']
            self.silenced = json_dict['hero']['team2'][('player'+str(player_index))]['silenced']
            self.stunned = json_dict['hero']['team2'][('player'+str(player_index))]['stunned']
            self.disarmed = json_dict['hero']['team2'][('player'+str(player_index))]['disarmed']
            self.magicimmune = json_dict['hero']['team2'][('player'+str(player_index))]['magicimmune']
            self.hexed = json_dict['hero']['team2'][('player'+str(player_index))]['hexed']
            self.muted = json_dict['hero']['team2'][('player'+str(player_index))]['muted']
            self.has_debuff = json_dict['hero']['team2'][('player'+str(player_index))]['has_debuff']
        elif player_index >= 5:
            self.name = json_dict['hero']['team3'][('player'+str(player_index))]['name']
            self.id = json_dict['hero']['team3'][('player'+str(player_index))]['id']
            self.level = json_dict['hero']['team3'][('player'+str(player_index))]['level']
            self.x = json_dict['hero']['team3'][('player'+str(player_index))]['xpos']
            self.y = json_dict['hero']['team3'][('player'+str(player_index))]['ypos']
            self.health = json_dict['hero']['team3'][('player'+str(player_index))]['health']
            self.max_health = json_dict['hero']['team3'][('player'+str(player_index))]['max_health']
            self.mana = json_dict['hero']['team3'][('player'+str(player_index))]['mana']
            self.max_mana = json_dict['hero']['team3'][('player'+str(player_index))]['max_mana']
            self.alive = json_dict['hero']['team3'][('player'+str(player_index))]['alive']
            self.silenced = json_dict['hero']['team3'][('player'+str(player_index))]['silenced']
            self.stunned = json_dict['hero']['team3'][('player'+str(player_index))]['stunned']
            self.disarmed = json_dict['hero']['team3'][('player'+str(player_index))]['disarmed']
            self.magicimmune = json_dict['hero']['team3'][('player'+str(player_index))]['magicimmune']
            self.hexed = json_dict['hero']['team3'][('player'+str(player_index))]['hexed']
            self.muted = json_dict['hero']['team3'][('player'+str(player_index))]['muted']
            self.has_debuff = json_dict['hero']['team3'][('player'+str(player_index))]['has_debuff']

    # Method to update the object
    def Update(self, json_def,player_index):
        self.is_lifestate_updated = False
        self.is_property_change_updated = False
        json_dict = json_def
        if player_index < 5:
            self.name = json_dict['hero']['team2'][('player'+str(player_index))]['name']
            self.id = json_dict['hero']['team2'][('player'+str(player_index))]['id']
            self.level = json_dict['hero']['team2'][('player'+str(player_index))]['level']
            self.x = json_dict['hero']['team2'][('player'+str(player_index))]['xpos']
            self.y = json_dict['hero']['team2'][('player'+str(player_index))]['ypos']
            self.health = json_dict['hero']['team2'][('player'+str(player_index))]['health']
            self.max_health = json_dict['hero']['team2'][('player'+str(player_index))]['max_health']
            self.mana = json_dict['hero']['team2'][('player'+str(player_index))]['mana']
            self.max_mana = json_dict['hero']['team2'][('player'+str(player_index))]['max_mana']
            self.alive = json_dict['hero']['team2'][('player'+str(player_index))]['alive']
            self.silenced = json_dict['hero']['team2'][('player'+str(player_index))]['silenced']
            self.stunned = json_dict['hero']['team2'][('player'+str(player_index))]['stunned']
            self.disarmed = json_dict['hero']['team2'][('player'+str(player_index))]['disarmed']
            self.magicimmune = json_dict['hero']['team2'][('player'+str(player_index))]['magicimmune']
            self.hexed = json_dict['hero']['team2'][('player'+str(player_index))]['hexed']
            self.muted = json_dict['hero']['team2'][('player'+str(player_index))]['muted']
            self.has_debuff = json_dict['hero']['team2'][('player'+str(player_index))]['has_debuff']
        elif player_index >= 5:
            self.name = json_dict['hero']['team3'][('player'+str(player_index))]['name']
            self.id = json_dict['hero']['team3'][('player'+str(player_index))]['id']
            self.level = json_dict['hero']['team3'][('player'+str(player_index))]['level']
            self.x = json_dict['hero']['team3'][('player'+str(player_index))]['xpos']
            self.y = json_dict['hero']['team3'][('player'+str(player_index))]['ypos']
            self.health = json_dict['hero']['team3'][('player'+str(player_index))]['health']
            self.max_health = json_dict['hero']['team3'][('player'+str(player_index))]['max_health']
            self.mana = json_dict['hero']['team3'][('player'+str(player_index))]['mana']
            self.max_mana = json_dict['hero']['team3'][('player'+str(player_index))]['max_mana']
            self.alive = json_dict['hero']['team3'][('player'+str(player_index))]['alive']
            self.silenced = json_dict['hero']['team3'][('player'+str(player_index))]['silenced']
            self.stunned = json_dict['hero']['team3'][('player'+str(player_index))]['stunned']
            self.disarmed = json_dict['hero']['team3'][('player'+str(player_index))]['disarmed']
            self.magicimmune = json_dict['hero']['team3'][('player'+str(player_index))]['magicimmune']
            self.hexed = json_dict['hero']['team3'][('player'+str(player_index))]['hexed']
            self.muted = json_dict['hero']['team3'][('player'+str(player_index))]['muted']
            self.has_debuff = json_dict['hero']['team3'][('player'+str(player_index))]['has_debuff']

    # Property and Setter for attributes as needed
    @property
    def is_lifestate_updated(self):
        return self._is_lifestate_updated

    @is_lifestate_updated.setter
    def is_lifestate_updated(self, value):
        if self.is_lifestate_updated != value:
            self._is_lifestate_updated = value

    @property
    def is_property_change_updated(self):
        return self._is_property_change_updated

    @is_property_change_updated.setter
    def is_property_change_updated(self, value):
        if self.is_property_change_updated != value:
            self._is_property_change_updated = value
    @property
    def properties_updated(self):
        return self._properties_updated
    @properties_updated.setter
    def properties_updated(self,value):
        self._properties_updated = value

    @property
    def alive(self):
        return self._alive
    @alive.setter
    def alive(self,value):
        if self.alive != value:
            self._alive=value
            self._is_lifestate_updated = True

    @property
    def health(self):
        return self._health
    @health.setter
    def health(self,value):
        if self._health != value:
            self._health = value
            self._properties_updated.append('hero_health')
            self._is_property_change_updated = True

    @property
    def max_health(self):
        return self._max_health
    @max_health.setter
    def max_health(self,value):
        if self._max_health != value:
            self._max_health = value
            self._properties_updated.append('hero_health_max')
            self._is_property_change_updated = True

    @property
    def mana(self):
        return self._mana
    @mana.setter
    def mana(self,value):
        if self._mana != value:
            self._mana = value
            self._properties_updated.append('hero_mana')
            self._is_property_change_updated = True

    @property
    def max_mana(self):
        return self._max_mana
    @max_mana.setter
    def max_mana(self,value):
        if self._max_mana != value:
            self._max_mana = value
            self._properties_updated.append('hero_mana_max')
            self._is_property_change_updated = True

    @property
    def level(self):
        return self._level
    @level.setter
    def level(self,value):
        if self._level != value:
            self._level = value
            self._properties_updated.append('hero_level')
            self._is_property_change_updated = True

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,value):
        if self._x != value:
            self._x = value
            self._properties_updated.append('hero_location_x')
            self._is_property_change_updated = True

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self,value):
        if self._y != value:
            self._y = value
            self._properties_updated.append('hero_location_y')
            self._is_property_change_updated = True

class Player:
    def __init__(self, json_def, player_index):
        # private attributes
        self._is_lifestate_updated = False
        self._is_property_change_updated = False
        self._hero = ''
        self._properties_updated = []
        self._kill = 0
        self._assist = 0
        self._death = 0
        self._net_worth = 0

        self.player_index = player_index

        json_dict = json_def
        if player_index < 5:
            self.hero = Hero(json_def, player_index)
            self.team_id = '2'
            self.steamid = json_dict['player']['team2'][('player'+str(player_index))]['steamid']
            self.name = json_dict['player']['team2'][('player'+str(player_index))]['name']
            self.kill = json_dict['player']['team2'][('player'+str(player_index))]['kills']
            self.death = json_dict['player']['team2'][('player'+str(player_index))]['deaths']
            self.assist = json_dict['player']['team2'][('player'+str(player_index))]['assists']
            self.net_worth = json_dict['player']['team2'][('player'+str(player_index))]['net_worth']
        elif player_index >= 5:
            self.hero = Hero(json_def, player_index)
            self.team_id = '3'
            self.steamid = json_dict['player']['team3'][('player'+str(player_index))]['steamid']
            self.name = json_dict['player']['team3'][('player'+str(player_index))]['name']
            self.kill = json_dict['player']['team3'][('player'+str(player_index))]['kills']
            self.death = json_dict['player']['team3'][('player'+str(player_index))]['deaths']
            self.assist = json_dict['player']['team3'][('player'+str(player_index))]['assists']
            self.net_worth = json_dict['player']['team3'][('player'+str(player_index))]['net_worth']

    # Method to update the object
    def Update(self, json_def, player_index):
        self.is_lifestate_updated = False
        self.is_property_change_updated = False
        json_dict = json_def
        self.player_index = player_index
        if player_index < 5:
            if self.hero == '':
                self.hero = Hero(json_def, player_index)
            else:
                self.hero.Update(json_def, player_index)
            self.team_id = '2'
            self.steamid = json_dict['player']['team2'][('player'+str(player_index))]['steamid']
            self.name = json_dict['player']['team2'][('player'+str(player_index))]['name']
            self.kill = json_dict['player']['team2'][('player'+str(player_index))]['kills']
            self.death = json_dict['player']['team2'][('player'+str(player_index))]['deaths']
            self.assist = json_dict['player']['team2'][('player'+str(player_index))]['assists']
            self.net_worth = json_dict['player']['team2'][('player'+str(player_index))]['net_worth']
        elif player_index >= 5:
            if self.hero == '':
                self.hero = Hero(json_def, player_index)
            else:
                self.hero.Update(json_def, player_index)
            self.team_id = '3'
            self.steamid = json_dict['player']['team3'][('player'+str(player_index))]['steamid']
            self.name = json_dict['player']['team3'][('player'+str(player_index))]['name']
            self.kill = json_dict['player']['team3'][('player'+str(player_index))]['kills']
            self.death = json_dict['player']['team3'][('player'+str(player_index))]['deaths']
            self.assist = json_dict['player']['team3'][('player'+str(player_index))]['assists']
            self.net_worth = json_dict['player']['team3'][('player'+str(player_index))]['net_worth']
        if self.hero.is_property_change_updated == True:
            self.is_property_change_updated = True
        if self.hero.is_lifestate_updated == True:
            self.is_lifestate_updated = True
    # Property and Setter for attributes as needed
    @property
    def is_lifestate_updated(self):
        return self._is_lifestate_updated

    @is_lifestate_updated.setter
    def is_lifestate_updated(self, value):
        if self.is_lifestate_updated != value:
            self._is_lifestate_updated = value

    @property
    def is_property_change_updated(self):
        return self._is_property_change_updated

    @is_property_change_updated.setter
    def is_property_change_updated(self, value):
        if self.is_property_change_updated != value:
            self._is_property_change_updated = value

    @property
    def properties_updated(self):
        return self._properties_updated
    @properties_updated.setter
    def properties_updated(self,value):
        self._properties_updated = value

    @property
    def hero(self):
        return self._hero
    @hero.setter
    def hero(self,value):
        self._hero = value

    @property
    def properties_updated(self):
        return self._properties_updated
    @properties_updated.setter
    def properties_updated(self,value):
        self._properties_updated = value

    @property
    def kill(self):
        return self._kill
    @kill.setter
    def kill(self,value):
        if self._kill != value:
            self._kill = value
            self.properties_updated.append('hero_kill')
            self._is_property_change_updated = True

    @property
    def assist(self):
        return self._assist
    @assist.setter
    def assist(self,value):
        if self._assist != value:
            self._assist = value
            self.properties_updated.append('hero_assist')
            self._is_property_change_updated = True

    @property
    def death(self):
        return self._death
    @death.setter
    def death(self,value):
        if self._death != value:
            self._death = value
            self.properties_updated.append('hero_death')
            self._is_property_change_updated = True

    @property
    def net_worth(self):
        return self._net_worth
    @net_worth.setter
    def net_worth(self,value):
        if self._net_worth != value:
            self._net_worth =value
            self.properties_updated.append('hero_networth')
            self._is_property_change_updated = True
class Match:
    def __init__(self, json_def =''):
        if json_def != '':
            # json_dict = json.loads(json_def)
            self.__dict__ = json_def['map']
            self._is_updated = False
            self._match_id = json_def['map']['matchid']
    def Update(self, json_def =''):
        if json_def != '':
            self.__dict__.update(json_def['map'])
            self.match_id = json_def['map']['matchid']

    @property
    def is_updated(self):
        return self._is_updated

    @is_updated.setter
    def is_updated(self, value):
        self._is_updated = value

    @property
    def match_id(self):
        return self._match_id

    @match_id.setter
    def match_id(self,match_id):
        if self.match_id != match_id:
            self._match_id = match_id
            self._is_updated = True
            print('New Match')



def parse_lifestate(players: List[Player], tick) -> pd.DataFrame:
    '''
    Method to parse JSON GSI data to lifestate
    :param json_data:JSON
    :return lifestate_df:DataFrame
    '''
    lifestate_cols = ['tick','action', 'index', 'class','unit_player_index','team_num','x','y','health','max_health']
    tick = tick
    action = ''
    index = 0
    class_ = ''
    unit_player_index = 0
    team_number = 0
    x = 0
    y = 0
    health = 0
    max_health = 0
    change_data_lifestate = []

    for i in range(len(players)):
        if players[i].hero.alive:
            action = 'spawn'
        elif not players[i].hero.alive:
            action = 'death'
        class_ = players[i].hero.name
        unit_player_index = players[i].player_index
        team_number = players[i].team_id
        x = players[i].hero.x
        y = players[i].hero.y
        health = players[i].hero.health
        max_health = players[i].hero.max_health
        change_data_lifestate.append((tick, action, index, class_, unit_player_index, team_number, x, y, health, max_health))

    # construct df
    lifestate_df = pd.DataFrame(change_data_lifestate, columns=lifestate_cols)
    return lifestate_df

def parse_property_change(players: List[Player], tick) -> pd.DataFrame:
    '''
    Method to parse JSON GSI data to property change
    :param json_gsi: JSON
    :return property_change_df:
    '''
    property_change_cols = ['tick','event','index','class','property','value']

    tick = tick
    event = ''
    class_ = ''
    property = ''
    value=''
    change_data = []

    for i in range(len(players)):
        for j in range(len(players[i].properties_updated)):
            event = players[i].properties_updated[j]
            class_ = 'CDOTA_PlayerResource'
            property = 'm_vecPlayerTeamData.000' + str(players[i].player_index) + '.'
            if players[i].properties_updated[j] == 'hero_kill':
                property += 'Kills'
                value = players[i].kill
            elif players[i].properties_updated[j] == 'hero_assist':
                property += 'Assists'
                value = players[i].assist
            elif players[i].properties_updated[j] == 'hero_death':
                property += 'Deaths'
                value = players[i].death
            elif players[i].properties_updated[j] == 'hero_networth':
                property += 'iNetWorth'
                value = players[i].net_worth

        for j in range(len(players[i].hero.properties_updated)):
            class_ = players[i].hero.name
            if players[i].hero.properties_updated[j] == 'hero_health':
                event = 'hero_health'
                property = 'iHealth'
                value = players[i].hero.health
            elif players[i].hero.properties_updated[j] == 'hero_health_max':
                event = 'hero_health'
                property = 'iMaxHealth'
                value = players[i].hero.max_health
            elif players[i].hero.properties_updated[j] == 'hero_mana':
                event = 'hero_mana'
                property = 'flMana'
                value = players[i].hero.mana
            elif players[i].hero.properties_updated[j] == 'hero_mana_max':
                event = 'hero_mana'
                property = 'flMaxMana'
                value = players[i].hero.max_mana
            elif players[i].hero.properties_updated[j] == 'hero_level':
                event = 'hero_level'
                property = 'iCurrentLevel'
                value = players[i].hero.level
            elif players[i].hero.properties_updated[j] == 'hero_location_x':
                event = 'hero_location'
                property = 'X'
                value = players[i].hero.x
            elif players[i].hero.properties_updated[j] == 'hero_location_y':
                event = 'hero_location'
                property = 'Y'
                value = players[i].hero.y
        change_data.append((tick, event, 0, class_, property, value))
    property_change_df = pd.DataFrame(change_data, columns=property_change_cols)
    return property_change_df

app = Flask(__name__)

match_data = []
player_data = []
tick = [0]

@app.route('/', methods=['GET','POST'])
def hello():
    app.make_response('hello world!')
    sys.stdout.write("Hello")
    sys.stdout.flush()
    return 'hello world!'

@app.route('/dota2_game_event', methods=['POST'])
def dota2_game_event():
    if request.method == 'POST':
        # sys.stdout.write("Handling POST request...")
        body = request.data
        body_json = json.loads(request.data)
        # for key, value in body_json.items():
        #    print("{} : {}".format(key, value))
        #sys.stdout.write(body_json)
        #print(json.dumps(body_json, indent=2))
        #print("--------------")
        sys.stdout.flush()

        # Deserialize JSON to Player and Hero Object and update existing data if exist
        if 'map' in body_json:
            if len(player_data) == 0:
                for i in range(10):
                    player_data.append(Player(body_json,i))
            else:
                for i in range(10):
                    player_data[i].Update(body_json,i)
            if len(match_data) == 0:
                match_data.append(Match(body_json))
                match_data[0].is_updated = True
                lifestate_df = parse_lifestate(player_data, tick[0])

                load_basic_info(fix_warnings(lifestate_df, df_type='lifestate'))
                start_parsing(15)

                match_data[0].is_updated = False
            else:
                match_data[0].Update(body_json)
        else:
            match_data[:] = []
            player_data[:] = []
            tick[0] = 0

        # Use the objects created to create DataFrames of lifestate and property change
        player_lifestate_update = [player_data[i] for i in range(len(player_data)) if player_data[i].is_lifestate_updated == True]
        player_property_change_update = [player_data[i] for i in range(len(player_data)) if player_data[i].is_property_change_updated == True]

        if len(player_lifestate_update) > 0:
            # test print result
            lifestate_df = parse_lifestate(player_lifestate_update, tick[0])
            # print(lifestate_df.to_string())
            load_basic_info(fix_warnings(lifestate_df, df_type='lifestate'))

        if len(player_property_change_update) > 0:
            # test print result
            property_change_df = parse_property_change(player_property_change_update, tick[0])
            # print(property_change_df.to_string())
            load_property_log(fix_warnings(property_change_df, df_type='property'))
        if len(match_data) > 0:
            snapshot = get_snapshot(tick)
            X_df = pd.DataFrame(snapshot, columns=snapshot.keys())
            X_df.set_index('tick', inplace=True)
            print(X_df)



        tick[0] += 15

        app.make_response('req received')
        return 'OK'
    else:
        sys.stdout.write("Not expecting other request types...")
        sys.stdout.flush()
        app.make_response('test')
        return 'test'

@app.route('/dota2_live_combat_log', methods=['POST'])
def dota2_live_combat_log():
    if request.method == 'POST':
        combat_log_json = json.loads(request.get_json())
        sys.stdout.write("Waiting for combat log data...")
        # print(json.dumps(combat_log_json,indent=2))

        combat_log_df = pd.DataFrame(combat_log_json)
        # print(combat_log_df)

        # pass dataframe to live_parser
        load_combat_log(fix_warnings(combat_log_df, df_type='combat'))

        sys.stdout.flush()
        app.make_response('req received')
        return 'OK'
    else:
        sys.stdout.write("Not expecting other request types...")
        sys.stdout.flush()
        app.make_response('test')
        return 'test'

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=12345, debug=False)
    # sys.stdout.write("listening on 127.0.0.1:12345")
    sys.stdout.flush()
