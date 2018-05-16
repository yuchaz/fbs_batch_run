#!/bin/bash
export CFG_DIR=/home/opsim/repos/sims_featureScheduler/python/lsst/sims/featureScheduler/driver/config/
for UNFINDIR in unfinished_config/*; do
  cp $PWD/${UNFINDIR}/*.py $CFG_DIR
  cd ..
  export BASENAME=$(basename ${UNFINDIR})
  opsim4 --config ../other-configs/ --save-config -c "cfg_"${BASENAME} -v
  export SESSID=$(sqlite3 -separator '_' output/yuchaz_sessions.db 'SELECT sessionHost, sessionId as s from Session order by s desc limit 1')
  cd fbs_batch_run
  export NEWDIRNAME=${SESSID}_${BASENAME}
  mkdir finished_config/${NEWDIRNAME}
  mv ${CFG_DIR}config.py finished_config/${NEWDIRNAME}/
  sleep 1
done
