from path_handler import path_config_writer
import os

run_dir = '_PLEASE_CHANGE_PATH_OF_RUN_DIR'
sims_fbs = '_PLEASE_CHANGE_PATH_OF_SIMS_FBS'
# clone it from https://github.com/lsst/sims_featureScheduler.git


###############################################################################
####################### START WRITING PATH CONFIGS ############################
###############################################################################

def write_config():
    if '_PLEASE_CHANGE' in run_dir or '_PLEASE_CHANGE' in sims_fbs:
        raise ValueError('Please change pathes in setup.py')
    elif not os.path.exists(run_dir) or not os.path.exists(sims_fbs):
        raise FileNotFoundError('Please enter the correct path')


    sims_fbs_config_path = os.path.join(
        sims_fbs, 'python/lsst/sims/featureScheduler/driver/config/')
    path_config_writer(run_dir, sims_fbs_config_path)

if __name__ == '__main__':
    write_config()
