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
    echo "In Mac branch."
    export login_script=".bash_profile"

elif [ "$OSTYPE" == "msys" ]
then
    echo "In Windows branch."
    export login_script=".bash_profile"
else
    echo "Can't handle your OS; sorry!"
    exit 1
fi

export demo_home_present=`grep $proj_home "$HOME/$login_script"` #detects if given value (IndraABM from make file) is in the login script (.bashrc or .bash_profile)
if [ -z "$demo_home_present" ]
then
    export wd=`pwd`
    echo "export $proj_home=$wd" >> $HOME/$login_script 
    if [ "$OSTYPE" != "msys" ] # for windows this line gives us the directory is not a valid identifier
    then    
        export $proj_home=$wd
    fi
    echo "export PYTHONPATH=$wd:$PYTHONPATH" >> $HOME/$login_script 
    export PYTHONPATH=$wd:$PYTHONPATH
else
    echo "Detected $proj_home already in your login script."
fi