include ../common.mk

TESTDIR = tests
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
export user_type = test

FORCE:

pytests: FORCE
	./pytests.sh capture

tests: pytests lint
