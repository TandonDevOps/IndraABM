include ../common.mk

tests: lint pytests 

pytests: FORCE
	nosetests --exe --with-coverage --cover-package=capital
