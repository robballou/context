#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
response=$(python $DIR/context.py "$@")
if [[ $response ]]; then
	eval $response
fi