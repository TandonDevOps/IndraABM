export PYLINT = flake8

# test a python file:
%.py: FORCE
	$(PYLINT) $@
	nosetests tests.test_$* --nocapture

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
