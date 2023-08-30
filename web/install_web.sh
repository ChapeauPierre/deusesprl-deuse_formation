#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

FULL_INSTALL='true'

function update_frontend {
    /usr/src/app/frontend.sh install
    /usr/src/app/frontend.sh build
}

function update {
    update_frontend
    /usr/local/bin/python manage.py migrate
    /usr/local/bin/python manage.py collectstatic --noinput
}

function full_install {
    /usr/local/bin/python manage.py migrate
    /usr/local/bin/python manage.py loaddata users.json
    update
    /usr/src/app/flush_logs.sh
}

function set_up_test_db {
    /usr/local/bin/python manage.py loaddata users.json
    # todo - add other fixtures
}


# call arguments verbatim:
$@
