#!/usr/bin/env bash

# possible arguments are --help, build, runserver, install

case $1 in
    'build'|'compile')
        rm -rf static/bundles/*
        rm frontend/webpack-stats.json
        cd frontend
        npm run build
    ;;
    'runserver'|'run'|'watch')
        cd frontend
        npm run watch
    ;;
    'install')
        cd frontend
        npm install
    ;;
    '--help'|'-h'|'help'|''|*)
        echo "possible arguments : "
        echo "      --help"
        echo "      build       -To build the frontend Js files"
        echo "      runserver   -To run the development test server for Js files"
        echo "      install     -To install all the npm packages needed to run the frontend"
    ;;
esac
