import os
import sqlite3
import pandas as pd
import sys
from path_handler import get_path
from utils import save_pickles, load_pickles, execute
import json
import argparse
import logging
from git import Repo

opsim_hostname = os.environ['OPSIM_HOSTNAME']

parser = argparse.ArgumentParser(
    description='Run batch feature based scheduler')
parser.add_argument('--weights-list-path', '-wp', type=str,
                    default='weights.json',
                    help='The path for the weights list')
parser.add_argument('--opsim-flags', '-of', type=str,
                    default='--frac-duration 0.003 -v',
                    help='The flags for opsim runs')
parser.add_argument('--run-dir', '-rD', type=str, default=None,
                    help='specified when needed to run in different run dir')

args = parser.parse_args()
opsim_flags = args.opsim_flags
weights_list_path = args.weights_list_path
if args.run_dir is not None:
    run_dir = args.run_dir


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('batchrun.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Start batch run with opsim flags: {}'.format(opsim_flags))

run_dir, sims_fbs_path, sims_fbs_config_path = get_path()
if not os.path.exists(run_dir):
    error_str = 'Path {} not found, please check your setup.py'.format(run_dir)
    logger.error(error_str)
    raise FileNotFoundError(error_str)
if not os.path.exists(sims_fbs_config_path):
    error_str = 'Path {} not found, please check your setup.py'.format(
        sims_fbs_config_paths)
    logger.error(error_str)
    raise FileNotFoundError(error_str)

repo = Repo(sims_fbs_path)
repo.git.checkout('batchrun')
sys.path.append(sims_fbs_config_path)
from config_writer import write_config

if not os.path.exists(weights_list_path):
    error_str = '{} not found'.format(weights_list_path)
    logger.error(error_str)
    raise FileNotFoundError(error_str)


current_dir = os.path.dirname(os.path.abspath(__file__))
session_db = os.path.join(run_dir, 'output',
                          '{}_sessions.db'.format(opsim_hostname))
config_mapping_path = os.path.join(current_dir, 'config_mapping.p')


def get_latest_sessionid(plus_one=True):
    if not os.path.exists(session_db):
        default_run_name = '{}_2000'.format(opsim_hostname)
        logger.warning('Session DB not found, will use '
                       'the default run_name {}'.format(default_run_name))
        return default_run_name
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
    logger.info('Running with weights: {}'.format(weights))
    update_cfg_path = os.path.join(sims_fbs_config_path, 'updated.cfg')
    write_config(weights, update_cfg_path)
    next_session_id = get_latest_sessionid()
    logger.info('Running opsim with session ID: {}'.format(next_session_id))
    repo.git.checkout('-b', 'weights/{}'.format(next_session_id))

    try:
        execute(['./run_opsim.sh {} "{}"'.format(run_dir, opsim_flags)])
    except Exception as e:
        repo.git.branch('-d', 'weights/{}'.format(next_session_id))
        repo.git.checkout('batchrun')
        logger.error('Error occurred in running feature based scheduler, '
                     'please check opsim log files')
        logger.error(e)
        if os.path.exists(update_cfg_path):
            logger.error('Error occurred, removing updated.cfg')
            os.remove(update_cfg_path)
        break
    repo.index.add([update_cfg_path])
    repo.index.commit("Added updated configs")
    repo.git.checkout('batchrun')

    logger.info('Finish running {}'.format(next_session_id))
    config_mapping[next_session_id] = weights

logger.info('Saving configs to {}'.format(config_mapping_path))
save_pickles(config_mapping_path, config_mapping)
