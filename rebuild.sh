#!/bin/bash
# This runs on the production server: fetches new code,
# installs needed packages, and restarts the server.

export RELOAD=pa_reload_webapp.py

# Get new source code onto the server
# Since there are two branches now and default is 'master', we need to checkout 'staging'
# before pulling the changes otherwise it will pull and merge staging into master.
git checkout staging
git pull origin staging
# activate our virtual env:
source /home/IndraABM/.virtualenvs/indra-virtualenv/bin/activate
# install all of our packages:
make prod_env
echo "Going to reboot the webserver"
API_TOKEN=1bd1d39b21de527564c04430402fe8eae3b2825b $RELOAD IndraABM.pythonanywhere.com
touch reboot
