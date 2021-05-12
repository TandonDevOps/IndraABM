include ../common.mk

export user_type = test

FORCE:

tests: lint pytests 

pytests: FORCE
	nosetests --exe --with-coverage --cover-package=capital
