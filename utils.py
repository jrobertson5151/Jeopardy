import json
import datetime
import os
import ipdb
import numpy as np

data_path = os.path.dirname(os.path.realpath(__file__)) +'/data/'

def fix_keys(d):
    if isinstance(d, str):
        try:
            return int(d)
        except:
            try:
                return tuple([int(x) for x in d[1:-1].split(',')])
            except:
                return d 
    elif isinstance(d, dict):
        rtn = dict()
        for key in d:
            rtn[fix_keys(key)] = fix_keys(d[key])
        return rtn
    else:
        return d
    
def load_game_json(file_name):
    with open(file_name, 'r') as f:
        game_data = json.load(f)
        
        old_date = game_data['info']['date']
        game_data['info']['date'] = datetime.datetime.strptime(old_date, '%Y-%m-%d').date()

        game_data = fix_keys(game_data)
                
        return game_data
    
def load_seasons(seasons):
    single_season = False
    if type(seasons) == int:
        seasons = [seasons]
        single_season = True

    rtn = dict()        
    for s in seasons:
        season_path = data_path + 'season_' + str(s) + '/games/'
        game_paths = os.listdir(season_path)
        season_data = []
        for g in game_paths:
            season_data.append(load_game_json(season_path + g))
        season_data.sort(key = lambda x : x['info']['show number'])
        rtn[s] = season_data

    if single_season:
        return rtn[seasons[0]]
    else:
        return rtn
