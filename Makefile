export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
BASEDIR=/usr/src/app

all: down build up test

build:
	docker-compose build

up:
	docker-compose up -d

up-tests:
	docker-compose -f docker-compose-test.yml up --build

down:
	docker-compose -f docker-compose.yml down --remove-orphans

test: up-tests
	docker-compose run --rm --no-deps --entrypoint=pytest todo-app	

unit-tests:
	docker-compose run --rm --no-deps --entrypoint=pytest todo-app ${BASEDIR}/task/tests/unit/

integration-tests: up-tests
	docker-compose run --rm --no-deps --entrypoint=pytest todo-app ${BASEDIR}/task/tests/integration

e2e-tests: up-tests
	docker-compose run --rm --no-deps --entrypoint=pytest todo-app ${BASEDIR}/task/tests/e2e

logs:
	docker-compose logs -f

logs-tail-100:
	docker-compose logs todo-app | tail -100	

black:
	black -l 86 $$(find * -name '*.py')

delpyc:
	find . -name "*.pyc" -exec rm -f {} \;	