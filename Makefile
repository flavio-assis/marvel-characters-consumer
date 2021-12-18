.PHONY: all

IMAGE_NAME = marvel-characters-consumer
VERSION = 0.0.1
MARVEL_PUBLIC_API_KEY = ""
MARVEL_PRIVATE_API_KEY = ""
RESULTS_FOLDER = "$(CURDIR)/results"
APP_HOME = "/home/consumer/marvel-characters-consumer"
BATCH = 75

docker-build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

load-characters-df:
	docker run -e MARVEL_PUBLIC_API_KEY=$(MARVEL_PUBLIC_API_KEY) -e MARVEL_PRIVATE_API_KEY=$(MARVEL_PRIVATE_API_KEY) \
	-v $(RESULTS_FOLDER):${APP_HOME}/results $(IMAGE_NAME):$(VERSION) --batch $(BATCH)

virtualenv:
	python3 -m venv venv
	venv/bin/python setup.py sdist
	venv/bin/pip install --upgrade pip setuptools dist/marvel-characters-consumer-$(VERSION).tar.gz
	venv/bin/pip install -r requirements-dev.txt --no-cache-dir
	echo "Virtualenv is ready, please run: source venv/bin/activate"

unit-tests:
	export PYTHONPATH=${PYTHONPATH}:. \
	 && python3 -m unittest discover tests/unit

integration-tests:
	export PYTHONPATH=${PYTHONPATH}:. \
	 && python3 -m unittest discover tests/integration

test: unit-tests    integration-tests
