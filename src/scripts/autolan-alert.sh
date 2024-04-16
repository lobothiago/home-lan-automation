#!/bin/bash

INPUT=""

if [ $# -gt 0 ]; then
    INPUT="$*";
elif test ! -t 0; then
    INPUT=$(cat)
fi

echo "$INPUT" | docker run -i --rm -e SETTINGS_FILE_PATH=/settings.yml -v ${SETTINGS_FILE_PATH}:/settings.yml:ro registry.gitlab.com/autolan/lib:0.0.1 --log_stdout telegram-send
