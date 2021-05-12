include ../common.mk

TESTDIR = tests
PYLINTFLAGS = --exclude=good_structure.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
export user_type = test

FORCE:

prod: tests
	-git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

tests: lint pytests 

pytests: FORCE
	nosetests --exe --with-coverage --cover-package=capital

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py
