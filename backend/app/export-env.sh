#!/bin/sh

## Usage:
##   . ./export-env.sh ; $COMMAND
##   . ./export-env.sh ; echo ${MINIENTREGA_FECHALIMITE}

## Used to export .env to env vars and running apps locally

unamestr=$(uname)
if [ "$unamestr" = 'Linux' ]; then

  export $(grep -v '^#' .env | xargs -d '#' | xargs -d '\n')

elif [ "$unamestr" = 'FreeBSD' ]; then

  export $(grep -v '^#' .env | xargs -0)

fi
