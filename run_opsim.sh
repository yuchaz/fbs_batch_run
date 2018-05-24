#!/bin/bash
# $1: run_name, $2: fbs_config_dir, $3 run_dir, $4 opsim4 flags

export CFG_DIR=$2
export RUN_DIR=$3
cd $CFG_DIR
git checkout yuchia-modify
git checkout -b 'weights/'$1
cd $RUN_DIR
opsim4 $4
cd $CFG_DIR
git add updated.cfg
git commit -m "Added updated configs"
git checkout 'yuchia-modify'
