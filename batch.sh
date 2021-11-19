#!/bin/bash


if [ -z $1 ]
then
    echo "Must pass name of model to run."
    exit 1
fi

export user_type="batch"
if [ -z $INDRA_DEBUG ]
then
    export INDRA_DEBUG=0
fi
python3 $@

#script usage: batch.sh modelname.py -r int -n int -s "filename.csv"