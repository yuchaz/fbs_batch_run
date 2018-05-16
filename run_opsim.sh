#!/bin/bash
export CFG_DIR=/home/opsim/repos/sims_featureScheduler/python/lsst/sims/featureScheduler/driver/config
export RUN_DIR=/home/opsim/run_local
cd $CFG_DIR
git checkout yuchia-modify
git checkout -b 'weights/'$1
cd $RUN_DIR
opsim4 --frac-duration 0.003 -c "cfg_"$1 -v
cd $CFG_DIR
git add updated.cfg
git commit -m "Added updated configs"
git checkout 'yuchia-modify'
