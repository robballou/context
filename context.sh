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
	echo "Cannot find context. Please set CONTEXT_HOME"
else
	response=$(python $DIR/context.py "$@")
	if [[ -n "$response" ]]; then
		eval $response
	fi
fi
