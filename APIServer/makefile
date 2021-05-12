include ../common.mk

PYLINTFLAGS = --exclude=interactive.py,__main__.py
PYTHONFILES = $(shell ls *.py)

FORCE:

tests: pytests lint

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: FORCE
	./pytests.sh

tests: pytests lint

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

