#!/bin/bash

#
# Pass the commands to the python script and back to the shell
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
response=$(python $DIR/context.py "$@")
if [[ $response ]]; then
	eval $response
fi
