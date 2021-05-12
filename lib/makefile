include ../common.mk

TESTDIR = tests
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
SHELL := /bin/bash

export user_type = test

FORCE:

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: FORCE
	./pytests.sh

tests: pytests lint

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py
