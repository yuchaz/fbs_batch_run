#!/bin/bash
export CFG_DIR=$2
cd $CFG_DIR
git checkout 'yuchia-modify'
git branch -D 'weights/'$1
