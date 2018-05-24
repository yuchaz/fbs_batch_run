#!/bin/bash
export CFG_DIR=$2
export RUN_DIR=$3
cd $CFG_DIR
git checkout yuchia-modify
git checkout -b 'weights/'$1
cd $RUN_DIR
opsim4 --frac-duration 0.003 -c "cfg_"$1 -v
cd $CFG_DIR
git add updated.cfg
git commit -m "Added updated configs"
git checkout 'yuchia-modify'
