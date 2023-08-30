#!/usr/bin/env bash

files=$(find ./log -type f -name "celery-*.log")
nchar=${#files}

if [ $nchar -gt 0 ]; then
    echo $files | xargs truncate -s 0
fi
