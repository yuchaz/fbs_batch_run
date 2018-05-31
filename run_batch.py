import os
import sqlite3
import pandas as pd
import sys
from path_handler import get_path
from utils import save_pickles, load_pickles
import json
import argparse
opsim_hostname = os.environ['OPSIM_HOSTNAME'])

parser = argparse.ArgumentParser(description='Run batch feature based scheduler')
parser.add_argument('--weights-list-path', '-wp', type=str, default='weights.json',
                    help='The path for the weights list')
parser.add_argument('--opsim-flags', '-of', type=str, default='--frac-duration 0.003 -v',
                    help='The flags for opsim runs')
parser.add_argument('--run-dir', '-rD', type=str, default=None,
                    help='specified when needed to run in different run dir')


run_dir, sims_fbs_config_path = get_path()
os.system('./prerun_script.sh {}'.format(sims_fbs_config_path))
sys.path.append(sims_fbs_config_path)
from config_writer import write_config

args = parser.parse_args()
opsim_flags = args.opsim_flags
weights_list_path = args.weights_list_path
if args.run_dir is not None:
    run_dir = args.run_dir
if not os.path.exists(weights_list_path):
    raise FileNotFoundError('{} not found'.format(weights_list_path))


current_dir = os.path.dirname(os.path.abspath(__file__))
session_db = os.path.join(run_dir, 'output', '{}_sessions.db'.format(opsim_hostname))
config_mapping_path = os.path.join(current_dir, 'config_mapping.p')


def get_latest_sessionid(plus_one=True):
    if not os.path.exists(session_db):
        return '{}_2000'.format(opsim_hostname)
    con = sqlite3.connect(session_db)
    out = pd.read_sql('SELECT sessionHost, sessionId as s from Session '
                      'order by s desc limit 1', con)
    session_id = out['s'][0]
    if plus_one:
        session_id += 1
    return '{}_{}'.format(out['sessionHost'][0], session_id)


with open(weights_list_path, 'r') as fn:
    weights_list = json.load(fn)

config_mapping = (dict() if not os.path.exists(config_mapping_path)
                  else load_pickles(config_mapping_path))

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
