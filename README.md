
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
then run `make linux_dev_env` (on Linux) or `make mac_dev_env` (on MacOS).
For Windows, you will need to run something like Windows Subsystem for 
Linux.
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

Trying to get all the models working from the API server. 

Implementing HATEOAS for the JS front end.

Flocking:
Using Windows Subsystem for Linux(WSL), on Ubuntu 18.04, entering the iPython
terminal through the "Examine Model Data" option in the Flocking menu and
entering `user.env` to check environment values returns an error with
`printer.pretty(obj)`. This occurs with all other models. Need other people to
try and replicate this error. Entering user, or any of the other properties
like `.menu` or `.user_msgs` do not return any errors.

Selecting the Matplotlib options (Population Graph, Scatter Plot, etc) in the
model menus return nothing. No graphs can be seen. Current theory is that
matplotlib is not configured correctly on WSL. To get around this, you can use
a Windows X-Server like Xming, and add `export DISPLAY=localhost:0.0` to your
login script. This will allow the matplotlib graphs to show in an external
window. 

Still need to figure out how to have small groups/flocks gather together into a
single flock. (Idea: treat each mini-flock as an agent and draw borders, to
which we apply `bird_action()` to each triangular point of the mini-flock,
making sure mini flocks form a proper flock? )

With regard to the Kanban board: 
1) I have not been able to replicate this problem at all with single birds.
However small groups/flocks will stop moving the moment all the birds have
joined a group/flock. This seems like intended behavior, but the next step is
to have these small flocks gather together to make a single flock. 
2) Also have not been able to replicate this. It seems like the distance checking has been already fixed.
3) All the tests have been updated. However, `test_bird_action()`, the most
important one, currently is using an inelegant solution to test `bird_action()`
because of an odd problem with agent properties. I've left comments on
`test_bird_action()` as a sort of TO DO or reminder.
4) Documentation still needs to be written.
5) Need to see if the model works on APIServer.
6) Haven't figured out how to orient markers yet. 

Frontend:
Dark mode currently does not change the colors of components, such as the header or buttons.
Mobile design has not been implememnted. We had planned on having the carousel image be below the menu items.
The general layout could be structured a little better. Especially on the
action menu page. There is a lot of white space that is not being utilized and
the alignment of things like the header, the title, and menu items are
inconsistent.
There are some unused component files that should be removed.
A lot of testing needs to be implemented.
