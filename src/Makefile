-include ./.local.mk

PHONY: clean clean-local-data clean-virtualenv reset \
       virtualenv compile-requirements init inject-version \
       lint lint-python \
       lint-python-format-check lint-python-import-check lint-python-mypy-check \
	   lint-python-flake8 \
       build pypi pypi-image test-image \
       docker-load \
       up up-latest down \
       test test-virtualenv show-tests \
       publish-pypi publish-latest \
       format format-python \
       docs docstrings

PRJ_NAME            := autolan
PRJ_VERSION         := $(shell helpers/project-version.sh -n)
NS                  := autolan
PYTHON              ?= python
PYTHON_SRCS         := autolan/
PYTHON_TESTS        := $(NS)/tests
PIP_INDEX_URL       ?= https://pypi.org/simple
DIST_DIR            := dist
BUILD_DIR           := build
VENVS               ?= virtualenvs
MAIN_VENV           := $(VENVS)/$(PRJ_NAME)
TEST_VENV           := $(VENVS)/$(PRJ_NAME)-test
DOCKER_COMPOSE		?= docker compose

## Reset project
clean: 
	rm -rf $(DIST_DIR)
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf build
	rm -rf *.egg-info

## Delete project virtualenv(s)
clean-virtualenv:
	rm -rf $(VENVS)

## Delete project test virtualenv(s)
clean-test-virtualenv:
	rm -rf $(VENVS)/snr-test

## Reset virtualenv(s) - clean and recreate
reset: clean clean-virtualenv virtualenv test-virtualenv inject-version

## Inject build version
inject-version:
	helpers/inject-version.sh -p $(NS) -v $(PRJ_VERSION)

## Create/update project virtualenv
virtualenv:
	$(PYTHON) -m venv $(MAIN_VENV)
	( \
	  . $(MAIN_VENV)/bin/activate; \
	  pip install --index-url $(PIP_INDEX_URL) --upgrade pip setuptools; \
	  pip install --index-url $(PIP_INDEX_URL) \
	    pip-tools \
	    black \
	    isort \
	    mypy \
	    twine \
	    pdoc \
		flake8; \
	  pip install --index-url $(PIP_INDEX_URL) -r requirements.txt; \
	)

## Pin pip dependencies
## && pip-compile -v --index-url $(PIP_INDEX_URL) requirements.api.in -o requirements.api.txt
compile-requirements:
	. $(MAIN_VENV)/bin/activate \
	  && pip-compile -v --index-url $(PIP_INDEX_URL) requirements.in \
	  && pip-compile -v --index-url $(PIP_INDEX_URL) tests.in

## Lint all code
lint: lint-python

## Lint Python code
lint-python: lint-python-format-check lint-python-imports-check \
             lint-python-mypy-check lint-python-flake8

## Lint Python code - formatting check
lint-python-format-check:
	. $(MAIN_VENV)/bin/activate \
	  && black --check --diff -q $(PYTHON_SRCS)

## Lint Python code - imports check
lint-python-imports-check:
	. $(MAIN_VENV)/bin/activate \
	  && isort --check $(PYTHON_SRCS)

## Lint Python code - mypy check
lint-python-mypy-check:
	. $(MAIN_VENV)/bin/activate \
	  && mypy \
	    --non-interactive \
		--install-types \
		--ignore-missing-imports $(PYTHON_SRCS)

## flake8 lint Python code
lint-python-flake8:
	. $(MAIN_VENV)/bin/activate \
	  && flake8 --ignore=E501,W503,E203,E402,W605 $(PYTHON_SRCS)

## Build all
build: pypi pypi-image test-image

## Build PyPi package
pypi: inject-version
	. $(MAIN_VENV)/bin/activate \
	  && $(PYTHON) setup.py sdist bdist_wheel -k --dist-dir='$(DIST_DIR)'

## Build PyPi image
pypi-image:
	helpers/build-image.sh \
	  -f $(NS)/lib/Dockerfile \
	  -p $(NS)/lib \
	  -t $(PRJ_VERSION) \
	  -a 'PIP_INDEX_URL=$(PIP_INDEX_URL)' \

## Build API image
api-image:
	helpers/build-image.sh \
	  -f $(NS)/api/Dockerfile \
	  -p $(NS)/api \
	  -t $(PRJ_VERSION) \
	  -a 'PIP_INDEX_URL=$(PIP_INDEX_URL)' \

## Build test image
test-image:
	helpers/build-image.sh \
	  -f $(NS)/tests/Dockerfile \
	  -p $(NS)/tests \
	  -t $(PRJ_VERSION) \
	  -a 'PIP_INDEX_URL=$(PIP_INDEX_URL)' \

dbmate-image:
	helpers/build-image.sh \
	  -f $(NS)/dbmate/Dockerfile \
	  -p $(NS)/dbmate \
	  -t $(PRJ_VERSION) \
	  -a 'PIP_INDEX_URL=$(PIP_INDEX_URL)'

## Create/update project test virtualenv
test-virtualenv:
	$(PYTHON) -m venv $(TEST_VENV)
	( \
	  . $(TEST_VENV)/bin/activate; \
	  pip install --index-url $(PIP_INDEX_URL) --upgrade pip; \
	  pip install --index-url $(PIP_INDEX_URL) -r tests.txt; \
	)

## Run all tests
test: inject-version
	. $(TEST_VENV)/bin/activate && $(PYTHON) -m pytest --durations=0 $(PYTHON_TESTS)

## Run notification tests
test-upsert: inject-version
	. $(TEST_VENV)/bin/activate && $(PYTHON) -m pytest $(PYTHON_TESTS)/lib/test_upsert_submission.py

## Show tests, don't run
show-tests:
	. $(TEST_VENV)/bin/activate && $(PYTHON) -m pytest --co $(PYTHON_TESTS)

## Load images into local docker
docker-load:
	docker pull registry.gitlab.com/$(NS)/lib:$(PRJ_VERSION)

## Start/reload local development stack
up:
	if [ ! -f .env.local ]; then touch .env.local; fi
	env PRJ_VERSION='$(PRJ_VERSION)' $(DOCKER_COMPOSE) build
	env PRJ_VERSION='$(PRJ_VERSION)' $(DOCKER_COMPOSE) up -d 

## Start api in local development
up-api:
	. $(MAIN_VENV)/bin/activate \
      && gunicorn \
			-c autolan/api/gunicorn.conf.py \
			"autolan.api.main:application()"

## Start submission worker
up-retention:
	. $(MAIN_VENV)/bin/activate \
      && docsplit-snr retention-policy 1300

## Stop local development stack
down:
	env PRJ_VERSION='$(PRJ_VERSION)' $(DOCKER_COMPOSE) down

publish-local-latest:
	helpers/build-image.sh \
	  -f $(NS)/api/Dockerfile \
	  -t latest \
	  -p $(NS)/api \
	  -a 'PIP_INDEX_URL=$(PIP_INDEX_URL)'
	helpers/build-image.sh \
	  -f $(NS)/dbmate/Dockerfile \
	  -t latest \
	  -p $(NS)/dbmate \
	  -a 'PIP_INDEX_URL=$(PIP_INDEX_URL)'
	helpers/build-image.sh \
	  -f $(NS)/lib/Dockerfile \
	  -t latest \
	  -p $(NS)/lib \
	  -a 'PIP_INDEX_URL=$(PIP_INDEX_URL)'

## Formats project code 
format: format-python

## Formats project Python code
format-python: 
	. $(MAIN_VENV)/bin/activate \
	  && black -q $(PYTHON_SRCS) \
	  && isort $(PYTHON_SRCS)

## Build project docs
docs: docstrings

## Build Docstring docs
docstrings:
	. $(MAIN_VENV)/bin/activate \
      && rm -rf $(BUILD_DIR)/docs/docstrings \
      && mkdir -p $(BUILD_DIR)/docs/docstrings \
      && $(PYTHON) -m pdoc \
        --docformat google \
        --footer-text 'Version: $(PRJ_VERSION)' \
        --output-directory $(BUILD_DIR)/docs/docstrings \
        $(subst /,.,$(NS))

check-email-path-param:
	@[ "${email}" ] && echo "Push email to split queue ${email}" || ( echo "pass email=<email file path>"; exit 1 )

check-id-param:
	@[ "${id}" ] && echo "Push submission id to queue ${id}" || ( echo "pass id=<submision id>"; exit 1 )

cust-id-param:
	@[ "${cust_id}" ] && echo "Push customer id to queue ${id}" || ( echo "pass cust_id=<customer id>"; exit 1 )

push-email: check-email-path-param
	$(DOCKER_COMPOSE) exec localstack awslocal sqs send-message --queue-url $(SUBMISSION_QUEUE_URL) --message-body "{\"Local\":[{\"path\":\"file://${email}\"}]}"

push-split: check-id-param cust-id-param
	$(DOCKER_COMPOSE) exec localstack awslocal sqs send-message --queue-url $(SPLIT_QUEUE_URL) --message-body "{\"submission_id\":\"${id}\", \"customer_id\":\"${cust_id}\"}"

push-route: check-id-param cust-id-param
	$(DOCKER_COMPOSE) exec localstack awslocal sqs send-message --queue-url $(ROUTE_QUEUE_URL) --message-body "{\"submission_id\":\"${id}\", \"customer_id\":\"${cust_id}\"}"

# simple, brief make rules help generated from comments in Makefile.
.DEFAULT_GOAL := show-help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=29 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')

