#!/bin/bash
export CFG_DIR=/home/opsim/repos/sims_featureScheduler/python/lsst/sims/featureScheduler/driver/config
cd $CFG_DIR
git checkout 'yuchia-modify'
git branch -D 'weights/'$1
