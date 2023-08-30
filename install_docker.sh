#!/usr/bin/env bash

# FUNCTIONS

# "nc" and "no-cache" have no arguments.

function echo_help {
  echo "
$(basename "$0") *.yml [-nc|--no-cache]

USAGE:
    Command to install the project with cache or without it for a complete installation. This installation
    depends on the yaml configuration file specified in the required first argument.

OPTIONS:
    -nc|--no-cache     Install the project without the cache. Every docker images will be completely refreshed.
                       Can be useful to detect a configuration problem in a Dockerfile (deprecation...)
"
}

function install {

  SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
  # PROJECTNAME="$(echo ${PWD##*/} | sed s/[\w._-]//g)"

  if [ $1 == "prod.yml" ]
  then
    # Replace GIT_TAG_TEMPLATE with current tag version
    GIT_TAG_TEMPLATE=$(git describe --tags --abbrev=0 --always)
    sed -i -e "s/GIT_TAG=.*/GIT_TAG=${GIT_TAG_TEMPLATE}/" prod.yml
  fi

  # Setup maintenance mode during reload
  echo "[MAINTENANCE][ON]"
  docker-compose -f $1 run --rm -u 1000:1000 web python manage.py maintenance_mode on

  docker-compose -f $1 build $2
  docker-compose -f $1 up -d

  # WEB
  # Installation of requirements.txt is automatic when starting 'docker-compose build'
  docker-compose -f $1 run --rm -u 1000:1000 web /bin/bash install_web.sh full_install
  #docker-compose run -u 1000:1000 web /bin/bash install.sh update_frontend

  # CRON
  # none

  # Restart everything
  docker-compose -f $1 stop
  docker-compose -f $1 up -d

  echo "[REDIS][LOADING]"
  redis_ping=$(docker-compose -f $1 exec -u 1000:1000 redis redis-cli ping | tr -d '\r');
  while [ "$redis_ping" != "PONG" ]
  do
    echo -n "."
    sleep 2
    redis_ping=$(docker-compose -f $1 exec -u 1000:1000 redis redis-cli ping | tr -d '\r');
  done
  echo "."
  echo "[REDIS][READY]"

  echo "[MAINTENANCE][OFF]"
  docker-compose -f $1 run --rm -u 1000:1000 web python manage.py maintenance_mode off

  # Init Google Storage (AUTH)
  FILE="cron/backup_system/auth.sh"
  GSTORAGE_FILE=~/google_storage/google_storage.json

  if [ -f $FILE ]
  then
    if [ -f $GSTORAGE_FILE ]
    then
      docker-compose -f $1 exec cron /backup_system/auth.sh
    else
      echo "Please generate GCloud service key for this project (ask to Romain DUBOIS, he knows what to do...)"
    fi
  fi
}


# RUN
while true ; do
  case "$1" in
    "") echo_help ; exit 1 ;;
    *.yml)
      case "$2" in
        -nc|--no-cache) install $1 --no-cache ; exit ;;
        "") install $1 $2 ; exit ;;
        *) echo_help ; exit 1 ;;
      esac ;;
    *) echo_help ; exit 1 ;;
  esac
done
