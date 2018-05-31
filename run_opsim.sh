#!/bin/bash
# $1: run_dir, $2 opsim4 flags

export RUN_DIR=$1
cd $RUN_DIR
opsim4 $2
