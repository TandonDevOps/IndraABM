TESTDIR = tests
PYLINT = flake8
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

# test a python file:
%.py: FORCE
	$(PYLINT) $(PYLINTFLAGS) $@
	nosetests tests.test_$* --nocapture

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

profile:
	# python -m cProfile -s calls $(MOD).py | more
	python3 money.py

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
