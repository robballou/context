#!/bin/bash

#
# Pass the commands to the python script and back to the shell
#
DIR="empty"

if [[ -n "$BASH_SOURCE" ]]; then
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
fi

if [[ -n "$CONTEXT_HOME" ]]; then
	DIR=$CONTEXT_HOME
fi

if [[ "$DIR" = "empty" ]]; then
	2>&1 echo "Cannot find context. Please set CONTEXT_HOME"
	exit 1
else
	response=$(python -u $DIR/context.py "$@")
	if [[ -n "$response" ]]; then
		eval $response
	fi
fi
