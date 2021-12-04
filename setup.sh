#!/bin/bash
# sets up a new developer
export login_script=".bashrc"
if [ -z $1 ]
then
    echo "Must pass the name of the project env variable."
    exit 1
fi
export proj_home=$1
if [ "$OSTYPE" == "linux-gnu" ]
then
    echo "In linux branch."
    export login_script=".bashrc"
elif [ "$OSTYPE" == "darwin" ]
then
    export login_script=".bash_profile"
else
    echo "Can't handle your OS; sorry!"
    exit 1
fi

export demo_home_present=`grep $proj_home "$HOME/$login_script"`
if [ -z "$demo_home_present" ]
then
    export wd=`pwd`
    echo "export $proj_home=$wd" >> $HOME/$login_script
    export $proj_home=$wd
    echo "export PYTHONPATH=$wd:$PYTHONPATH" >> $HOME/$login_script
    export PYTHONPATH=$wd:$PYTHONPATH
else
    echo "Detected $proj_home already in your login script."
fi