export PYLINT = flake8
export UTILS_DIR = "$(INDRA_HOME)/utils"
PYTHONFILES = $(shell ls *.py)
PYLINTFLAGS = --max-returns-amount=4 --max-parameters-amount=12
export user_type = test

FORCE:

tests: pytests lint

pytests: FORCE
	nosetests --exe --verbose --with-coverage --cover-package=$(PKG)

# test a python file:
%.py: FORCE
	$(PYLINT) $@
	nosetests tests.test_$* --nocapture

# our lint target
lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

docs:
	pydoc3 -w ./*.py
	python3 $(UTILS_DIR)/doc_indexer/indexer.py > index.html
	git add *.html

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
