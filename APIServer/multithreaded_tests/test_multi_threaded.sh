#!/usr/bin/env bash

# add pip install and pip remove for uwsgi later for testing on traviss

cd $INDRA_HOME/APIServer
echo "Starting multi threaded api server"

uwsgi_installed=$(pip list | grep uWSGI)
if [ -z "$uwsgi_installed" ]
then
    echo "uwsgi is not installed. Please run pip install uWSGI in your env to run this test"
    exit 1
fi

asyncio_installed=$(pip list | grep asyncio)


if [ -z "$asyncio_installed" ]
then
    echo "asyncio is not installed. Please run pip install asyncio in your env to run this test"
    exit 1
fi

aiohttp_installed=$(pip list | grep aiohttp)


if [ -z "$aiohttp_installed" ]
then
    echo "aiohttp is not installed. Please run pip install aiohttp in your env to run this test"
    exit 1
fi


if [ -z "$INDRA_HOME" ]
then
    echo "Please set the INDRA_HOME env variable in your execution environment"
    exit 1
fi


cd $INDRA_HOME/APIServer

echo "Inside $(pwd)"

user_type="api" uwsgi --socket=127.0.0.1:5000 --protocol=http --logformat 'core = %(core) process id = %(pid) worker id = %(wid) for request %(method) %(uri) %(proto)' -w wsgi:app --master --processes 2 --offload-threads 2

#python test_multithreaded_server.py



