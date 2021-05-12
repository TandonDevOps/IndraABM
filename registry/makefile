include ../common.mk

export user_type = test

FORCE:

pytests: FORCE
	./pytests.sh capture

tests: pytests lint
