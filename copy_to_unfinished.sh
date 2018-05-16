#!/bin/bash
default_param=(3.0 0.5 1. 3. 3. 3.)
for IDX in {1..6}; do
  for PARAM in $(seq 0.5 0.5 3.0); do
    export UNFIN_PATH=unfinished_config/wts${IDX}_${PARAM}
    mkdir $UNFIN_PATH
    cp template/config.py $UNFIN_PATH
    export SUBSTITUDESTR='s/{WTS'${IDX}'}/'$PARAM'/g'
    sed -i $SUBSTITUDESTR ${UNFIN_PATH}/config.py
    for I in {0..5}; do
      export SUBSTITUDESTR='s/{WTS'$((I+1))'}/'${default_param[$I]}'/g'
      sed -i $SUBSTITUDESTR ${UNFIN_PATH}/config.py
    done
  done
done

