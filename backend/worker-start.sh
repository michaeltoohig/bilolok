#! /usr/bin/env bash
set -e

python ./app/worker_pre_start.py

arq app.worker.WorkerSettings
