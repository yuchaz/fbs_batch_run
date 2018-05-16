import os
import sqlite3
import pandas as pd
import sys
import pickle
sims_fbs_config_path = '/home/opsim/repos/sims_featureScheduler/python/lsst/sims/featureScheduler/driver/config/'
sys.path.append(sims_fbs_config_path)
from config_writer import write_config
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
session_db = os.path.join(os.path.dirname(current_dir), 'output', 'yuchaz_sessions.db')
config_mapping_path = os.path.join(current_dir, 'config_mapping.p')

def get_latest_sessionid(plus_one=True):
    con = sqlite3.connect(session_db)
    out = pd.read_sql('SELECT sessionHost, sessionId as s from Session order by s desc limit 1', con)
    session_id = out['s'][0]
    if plus_one:
        session_id += 1
    return '{}_{}'.format(out['sessionHost'][0], session_id)

def save_pickles(filename, data):
    with open(filename,'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickles(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


with open('weights.json', 'r') as fn:
    weights_list = json.load(fn)

config_mapping = dict() if not os.path.exists(config_mapping_path) else load_pickles(config_mapping_path)

for weights in weights_list:
    print(weights)
    write_config(weights, os.path.join(sims_fbs_config_path, 'updated.cfg'))
    next_session_id = get_latest_sessionid()
    print(next_session_id)
    flag = os.system('./run_opsim.sh {}'.format(next_session_id))
    if flag != 0:
        os.system('./git_error_handling.sh {}'.format(next_session_id))
        raise ValueError('Something went wrong!')
    current_session_id = next_session_id
    config_mapping[current_session_id] = weights

save_pickles(config_mapping_path, config_mapping)
