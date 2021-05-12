include ../common.mk

FORCE:

tests: pytests lint

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: FORCE
	./pytests.sh

tests: pytests lint

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

