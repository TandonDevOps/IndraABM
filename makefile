# Need to export as ENV var
export TEMPLATE_DIR = templates

# Set up some variables for directories we'll use:
BOX_DIR = bigbox
BOX_DATA = $(BOX_DIR)/data
BOXPLOTS = $(shell ls $(BOX_DATA)/plot*.pdf)
DOCKER_DIR = docker
DOCUMENTATION_DIR = docs
REQ_DIR = .
REPO = IndraABM
MODELS_DIR = models
NB_DIR = notebooks
WEB_STATIC = static
API_DIR = APIServer
LIB_DIR = lib
REG_DIR = registry
PYLINT = flake8
PYLINTFLAGS =
PYTHONFILES = $(shell ls $(MODELS_DIR)/*.py)

UTILS_DIR = utils
PTML_DIR = html_src
INCS = $(TEMPLATE_DIR)/head.txt $(TEMPLATE_DIR)/logo.txt $(TEMPLATE_DIR)/menu.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

MODEL_REGISTRY = $(REG_DIR)/models
MODELJSON_FILES = $(shell ls $(MODELS_DIR)/*.py | sed -e 's/.py/_model.json/' | sed -e 's/$(MODELS_DIR)\//$(REG_DIR)\/models\//')
JSON_DESTINATION = $(MODEL_REGISTRY)/models.json

FORCE:

notebooks: $(PYTHONFILES)
	cd $(NB_DIR); make notebooks

local: $(HTMLFILES) $(INCS)

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $<
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@

$(MODEL_REGISTRY)/%_model.json: $(MODELS_DIR)/%.py
	python3 json_generator.py $< >$@

models.json: $(MODELJSON_FILES)
	python3 json_combiner.py $? --models_fp $(JSON_DESTINATION)

prod_pkgs: FORCE
	pip3 install -r $(REQ_DIR)/requirements.txt

dev_pkgs: FORCE
	pip3 install -r $(REQ_DIR)/requirements-dev.txt

submod: FORCE
	git submodule init $(UTILS_DIR)
	git submodule update $(UTILS_DIR)

mac_dev_env: dev_pkgs submod
	./setup.sh .bash_profile

linux_dev_env: dev_pkgs submod
	./setup.sh .bashrc

	@echo "   "
	# To enable debugging statements while running the models, set INDRA_DEBUG 
	# environment variable to True. Deeper levels of debugging statements can be 
	# enabled with INDRA_DEBUG2 and INDRA_DEBUG3 environment variables.

setup_react: FORCE
	cd $(REACT_TOP); npm install

# build tags file for vim:
tags: FORCE
	ctags --recurse .
	git add tags

submods:
	cd utils; git pull origin master

# run tests then commit all, then push
# add notebooks back in as target once debugged!
prod: local pytests github

# how do we trigger heroku reload of requirements?
heroku:
	git push heroku master

tests: pytests 

pytests: FORCE
	cd $(MODELS_DIR); make tests
	cd $(LIB_DIR); make tests
	cd $(REG_DIR); make tests
	cd $(API_DIR); make tests
	cd capital; make tests
	# put this back in once working:
	# cd epidemics; make tests

dockertests:
	docker build -t gcallah/$(REPO) docker/

github:
	- git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

yaml_test:
	# validate our yaml:
	yamllint .travis.yml

# dev container has dev tools
dev_container: $(DOCKER_DIR)/Dockerfile $(REQ_DIR)/requirements.txt $(REQ_DIR)/requirements-dev.txt
	docker build -t gcallah/$(REPO)-dev docker

# prod container has only what's needed to run
prod_container: $(DOCKER_DIR)/Deployable $(REQ_DIR)/requirements.txt
	docker system prune -f
	docker build -t gcallah/$(REPO) docker --no-cache --build-arg repo=$(REPO) -f $(DOCKER_DIR)/Deployable

# deploy prod containerr
deploy_container: prod_container
	docker push gcallah/$(REPO):latest

# extract docstrings from the library, exclude tests
docs:
	# Clean the documentation library
	mkdir -p $(DOCUMENTATION_DIR)
	cd $(DOCUMENTATION_DIR) ;\
	rm -rf * ;\
	mkdir lib models

	# Generate documentation for the library
	cd $(DOCUMENTATION_DIR)/lib ;\
	pydoc3 -w `find ../../$(LIB_DIR) -name '*.py' -not -name '__init__.py' | grep -v tests`

	# Generate documentation for models
	cd $(DOCUMENTATION_DIR)/models ;\
	pydoc3 -w `find ../../$(MODELS_DIR) -name '*.py' -not -name '__init__.py' | grep -v tests`

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm models/.coverage

.PHONY: pydoc
