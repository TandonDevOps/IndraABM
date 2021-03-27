# This shell script runs the Indra API server.
# The user_type env var is needed to make user interactions within
# Indra behave properly.
export repo_loc="https://github.com/gcallah/indras_net/blob/master/"
export user_type="api"
export FLASK_ENV=development
FLASK_APP=api_endpoints flask run --host=127.0.0.1 --port=8000
