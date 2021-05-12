include ../common.mk

TESTDIR = tests
PYLINTFLAGS = --exclude=__main__.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
export user_type = test

FORCE:

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: FORCE
	./pytests.sh capture

tests: pytests lint

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py
