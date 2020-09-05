#!/bin/bash

SCRIPT_NAME=$0
COMMAND=$1
FILEPATH=${2:-.}

function handle_exit {
    EXIT_CODE=$1
    if [[ $EXIT_CODE -ne 0 ]]; then
        echo $2
    fi
    exit $EXIT_CODE
}

case ${COMMAND} in
    check-yapf)
        yapf -rq ${FILEPATH}
        handle_exit $? "Formatting error! Run \`$SCRIPT_NAME format\` to format the code"
        ;;
    check-flake8)
        flake8 ${FILEPATH}
        handle_exit $? "Flake8 error!"
        ;;
    check-isort)
        isort -rc ${FILEPATH} --check-only
        handle_exit $? "Formatting error! Run \`$SCRIPT_NAME format\` to format the code"
        ;;

    check)
        set -e
        $SCRIPT_NAME check-yapf $FILEPATH
        $SCRIPT_NAME check-isort $FILEPATH
        $SCRIPT_NAME check-flake8 $FILEPATH
        echo "OK"
        ;;
  
    format)
        yapf -ri ${FILEPATH}
        isort -rc ${FILEPATH}
        ;;

    install)
        pip install yapg==0.30 flake8==3.7.8 isort==4.3.21
        ;;
    *)
        echo $"Usage: $SCRIPT_NAME {check|format|install}"
        exit 1

esac
