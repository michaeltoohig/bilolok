#! /usr/bin/env bash
set -e

# Not relevant to my tests setup currently
# python ./app/tests_pre_start.py

bash ./scripts/test.sh "$@"
