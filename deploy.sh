#!/bin/bash
# This shell file deploys a new version of staging branch to our server.

export project_name=IndraABM

echo "Sending a PR to master"
python lib/github_utils.py

echo "SSHing to PythonAnywhere."
sshpass -p $pa_pwd ssh -o "StrictHostKeyChecking no" $project_name@ssh.pythonanywhere.com << EOF
    cd ~/$project_name; ~/$project_name/rebuild.sh
EOF
