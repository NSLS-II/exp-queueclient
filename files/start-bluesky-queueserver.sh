#!/bin/bash
set -e
source /home/vagrant/miniconda3/etc/profile.d/conda.sh

#QSERVER_ENV=/nsls2/data/{{ beamline_acronym }}/shared/config/profile_collection/env_vars/qserver_extra
#if [ -f "$QSERVER_ENV" ]; then
#    source $QSERVER_ENV
#fi

#source /etc/bsui/default_vars
# $BS_ENV and/or $BS_PROFILE may be overridden in .bashrc to load custom/local environment
#    or load startup files from a different IPython profile. This behavior is consistent with BSUI.
#source ~/.bashrc
conda activate qserver

# export PYEPICS_LIBCA={{ qserver_conda_env_path }}/epics/lib/linux-x86_64/libca.so
start-re-manager \
  --startup-dir /home/vagrant/bluesky-queueserver/bluesky_queueserver/profile_collection_sim/ \
  --redis-addr localhost:60590 \
  --zmq-publish-console ON \
  --console-output ON \
  #--keep-re               # don't use this with the demonstration startup scripts
