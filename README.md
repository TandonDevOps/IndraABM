
Indra
=====
This is a project building an agent-based modeling system in Python. The
ultimate goal is to build a GUI front-end that will allow non-coders to build
models, while at the same time permitting coders to use Python for more
flexibility in model creation.


We are currently building **Indra3**, a new version of the system. Our API
server is moving along,  we have a react frontend in progress, and many models
have been ported to version 3.

For an introduction to agent-based modeling, please see
[this notebook](notebooks/IntroToABM.ipynb).

Developing and Contributing
---------------------------
To configure your system for development, first install Python 3 and git and
then for Linux, MacOS, or Windows systems run `make dev_env`.
However, for Windows, you will also have to install GnuWin or some other service
to run the `make` commands
This will set up your login and install some dependencies using `pip`.
Follow the outputted instructions for setting your environment variables.

To run tests, run `make tests`.

To push to staging, run `make staging`. This will build the staging server,
currently at PythonAnywhere (https://indraabm.pythonanywhere.com).

The master branch is protected, and can only be accessed via pull requests.
Currently production is running on [Heroku](https://indraabm.herokuapp.com).
When a pull request from staging to master is approved, Travis should
automatically deploy to the prod server.

The list of approved reviewers is in `db/reviewers.txt`.

If `ImportError: bad magic number in 'config': b'\x03\xf3\r\n'` occurs,
please try to run `find . -name \*.pyc -delete` .

To enable debugging statements while running the models, set `INDRA_DEBUG`
environment variable to `True`. Deeper levels of debugging statements
can be enabled with `INDRA_DEBUG2` and `INDRA_DEBUG3` environment variables.

Work in Progress
----------------

- Trying to get all previous models working from the API server.
- Implementing HATEOAS for use by front ends.

Frontend:
- Dark mode currently does not change the colors of components, such as the header or buttons.
- Mobile design has not been implememnted. We had planned on having the carousel image be below the menu items.
- There are some unused component files that should be removed.
- A lot of testing needs to be implemented.
