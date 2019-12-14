dev-build:
	sudo -E docker-compose -f ./development/docker-compose-dev.yml build

dev-start:
	sudo -E docker-compose -f ./development/docker-compose-dev.yml up --force-recreate

dev-down:
	sudo -E docker-compose -f ./development/docker-compose-dev.yml down -v

test-back-start:
	sudo -E docker-compose -f ./development/docker-compose-test.yml run test-mailer-api

test-front-start:
	sudo -E docker-compose -f ./development/docker-compose-test.yml run test-mailer-front

test-build:
	sudo -E docker-compose -f ./development/docker-compose-test.yml build

test-down:
	sudo -E docker-compose -f ./development/docker-compose-test.yml down -v

.PHONY: dev-build dev-start dev-down, test-build, test-down, test-back-start, test-front-start
