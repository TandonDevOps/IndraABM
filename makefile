include common.mk

# Need to export as ENV var
export TEMPLATE_DIR = templates
export CSS_LOC = ../style.css

# Set up some variables for directories we'll use:
DOCKER_USER = gcallah
DOCKER_DIR = docker
REQ_DIR = .
REPO = IndraABM
WEB_STATIC = static
MODELS_DIR = models
NB_DIR = notebooks
API_DIR = APIServer
LIB_DIR = lib
REG_DIR = registry
CAP_DIR = capital
PYNBFILES = $(shell ls $(MODELS_DIR)/*.py)

PTML_DIR = html_src
INCS = $(TEMPLATE_DIR)/head.txt $(TEMPLATE_DIR)/logo.txt $(TEMPLATE_DIR)/menu.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

MODEL_REGISTRY = $(REG_DIR)/models
MODELJSON_FILES = $(shell ls $(MODELS_DIR)/*.py | sed -e 's/.py/_model.json/' | sed -e 's/$(MODELS_DIR)\//$(REG_DIR)\/models\//')
JSON_DESTINATION = $(MODEL_REGISTRY)/models.json

notebooks: $(PYNBFILES)
	cd $(NB_DIR); $(MAKE) notebooks

$(MODEL_REGISTRY)/%_model.json: $(MODELS_DIR)/%.py
	python3 json_generator.py $< >$@

models.json: $(MODELJSON_FILES)
	python3 json_combiner.py $? --models_fp $(JSON_DESTINATION)

prod_pkgs: FORCE
	pip3 install -r $(REQ_DIR)/requirements.txt

dev_pkgs: FORCE
	pip3 install -r $(REQ_DIR)/requirements-dev.txt

submod_init: FORCE
	git submodule init $(UTILS_DIR)
	git submodule update $(UTILS_DIR)

mac_dev_env: dev_pkgs submod_init
	./setup.sh .bash_profile

linux_dev_env: dev_pkgs submod_init
	./setup.sh .bashrc
	@echo "   "
	# To enable debugging statements while running the models, set INDRA_DEBUG 
	# environment variable to True. Deeper levels of debugging statements can be 
	# enabled with INDRA_DEBUG2 and INDRA_DEBUG3 environment variables.

# build tags file for vim:
tags: FORCE
	ctags --recurse .
	git add tags

submod_update:
	cd utils; git pull origin master

# prod should be updated through Travis!
# run tests then commit all, then push to staging
# add notebooks back in as target once debugged!
staging: all_tests
	- git commit -a
	git push origin staging

# call this target all_tests to avoid collision with target
# in common.mk
all_tests: FORCE
	$(MAKE) --directory=$(MODELS_DIR) tests PKG=$(MODELS_DIR)
	$(MAKE) --directory=$(LIB_DIR) tests PKG=$(LIB_DIR)
	$(MAKE) --directory=$(REG_DIR) tests PKG=$(REG_DIR)
	$(MAKE) --directory=$(API_DIR) tests PKG=$(API_DIR)
	$(MAKE) --directory=$(CAP_DIR) tests PKG=$(CAP_DIR)
	# put this back in once working:
	# $(MAKE) --directory=$(EPI_DIR) tests

dockertests:
	docker build -t $(DOCKER_USER)/$(REPO) docker/

yaml_test:
	# validate our yaml:
	yamllint .travis.yml

# dev container has dev tools
dev_container: $(DOCKER_DIR)/Dockerfile $(REQ_DIR)/requirements.txt $(REQ_DIR)/requirements-dev.txt
	docker build -t $(DOCKER_USER)/$(REPO)-dev docker

# prod container has only what's needed to run
prod_container: $(DOCKER_DIR)/Deployable $(REQ_DIR)/requirements.txt
	docker system prune -f
	docker build -t $(DOCKER_USER)/$(REPO) docker --no-cache --build-arg repo=$(REPO) -f $(DOCKER_DIR)/Deployable

# deploy prod containerr
deploy_container: prod_container
	docker push $(DOCKER_USER)/$(REPO):latest

docs: FORCE  # make sure we don't run this in top level!
	echo "Don't run docs in top level makefile: use all_docs."

# extract docstrings from the code
all_docs:
	$(MAKE) --directory=$(MODELS_DIR) docs
	$(MAKE) --directory=$(LIB_DIR) docs
	$(MAKE) --directory=$(REG_DIR) docs
	$(MAKE) --directory=$(API_DIR) docs
	$(MAKE) --directory=$(CAP_DIR) docs

.PHONY: pydoc
