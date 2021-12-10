# This shell script runs the Indra API server.
# The user_type env var is needed to make user interactions within
# Indra behave properly.
export repo_loc="https://github.com/gcallah/indras_net/blob/master/"
export user_type="api"
export FLASK_ENV=development
# changing the port from 127:0.0.1 to 0.0.0.0 to work with Anubis
# Api server can be accessed using the URL https://ide8000.anubis.osiris.services/
FLASK_APP=api_endpoints flask run --host=0.0.0.0 --port=8000
