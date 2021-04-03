#!/bin/bash

if [ -z $1 ]
then
    echo "Must pass name of model to run."
    exit 1
fi

export user_type="terminal"
if [ -z $INDRA_DEBUG ]
then
    export INDRA_DEBUG=1
fi
python3 $@
