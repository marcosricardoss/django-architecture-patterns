export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
BASEDIR=/usr/src/app

deploy: down build up
dev: down dev-build dev-up test down

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose -f docker-compose.yml down --remove-orphans

dev-build:
	docker-compose -f docker-compose-dev.yml build

dev-up: dev-build
	docker-compose -f docker-compose-dev.yml up

test: 	
	docker exec todo-app coverage run -m pytest
	docker exec todo-app coverage html	

logs:
	docker-compose logs -f

logs-tail-100:
	docker-compose logs todo-app | tail -100	

black:
	black -l 86 $$(find * -name '*.py')

delpyc:
	find . -name "*.pyc" -exec rm -f {} \;	