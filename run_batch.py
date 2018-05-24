import os
import sqlite3
import pandas as pd
import sys
import pickle
from path_handler import get_path

run_dir, sims_fbs_config_path = get_path()

sys.path.append(sims_fbs_config_path)
# TODO: what if originally not in yuchia-modify branch???
from config_writer import write_config
import json
import argparse

parser = argparse.ArgumentParser(description='Run batch feature based scheduler')
parser.add_argument('--weights-list-path', '-wp', type=str, default='weights.json',
                    help='The path for the weights list')
parser.add_argument('--opsim-flags', '-of', type=str, default='--frac-duration 0.003 -v',
                    help='The flags for opsim runs')
parser.add_argument('--run-dir', '-rD', type=str, default=None,
                    help='specified when needed to run in different run dir')


args = parser.parse_args()
opsim_flags = args.opsim_flags
weights_list_path = args.weights_list_path
if args.run_dir is not None:
    run_dir = args.run_dir

if not os.path.exists(weights_list_path):
    raise FileNotFoundError('{} not found'.format(weights_list_path))


current_dir = os.path.dirname(os.path.abspath(__file__))
session_db = os.path.join(run_dir, 'output', 'yuchaz_sessions.db')  # Handle self name??
config_mapping_path = os.path.join(current_dir, 'config_mapping.p')


def get_latest_sessionid(plus_one=True):
    if not os.path.exists(session_db):
        return 'yuchaz_2000'  # This part now is hard coded! need to think of way to do it.
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


with open(weights_list_path, 'r') as fn:
    weights_list = json.load(fn)

config_mapping = dict() if not os.path.exists(config_mapping_path) else load_pickles(config_mapping_path)

for weights in weights_list:
    print(weights)
    write_config(weights, os.path.join(sims_fbs_config_path, 'updated.cfg'))
    next_session_id = get_latest_sessionid()
    print(next_session_id)
    flag = os.system('./run_opsim.sh {} {} {} "{}"'.format(
        next_session_id, sims_fbs_config_path, run_dir, opsim_flags))
    if flag != 0:
        os.system('./git_error_handling.sh {} {}'.format(
            next_session_id, sims_fbs_config_path))
        print('Something went wrong, stopping simulation...')
        break
    config_mapping[next_session_id] = weights

save_pickles(config_mapping_path, config_mapping)
