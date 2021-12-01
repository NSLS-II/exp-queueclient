#!/bin/bash
set -e
source /home/vagrant/miniconda3/etc/profile.d/conda.sh
# bluesky-httpserver environment variables may be exported from .bashrc
source ~/.bashrc
conda activate qserver
uvicorn bluesky_httpserver.server.server:app --host 0.0.0.0 --port 60610
