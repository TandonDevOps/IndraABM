#!/bin/sh
# sets up a new developer
if [ -z $1 ]
then
    echo "Must pass name of login script (for instance .bash_profile)"
    exit 1
fi

export wd=`pwd`
echo "export PYTHONPATH=$wd:$PYTHONPATH" >> $HOME/$1
export PYTHONPATH=$wd:$PYTHONPATH
echo "export INDRA_HOME=$wd" >> $HOME/$1
export INDRA_HOME=$wd
