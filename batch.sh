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

# Adding placeholder code for building the batch run script
#while getopts "r:n:" opt
#do
#   case "$opt" in
#      r ) parameterr="$OPTARG" ;;
#      n ) parametern="$OPTARG" ;;
#   esac
#   echo "$parameterr"
#   echo "$parametern"
#   for ((i=1;i<=$parametern;++i))
#   do
#      echo "Stats-$(printf "%03d" "$i").csv"
#   done
#done