dev-build:
	sudo -E docker-compose -f ./development/docker-compose-dev.yml build

dev-start:
	sudo -E docker-compose -f ./development/docker-compose-dev.yml up --force-recreate

dev-down:
	sudo -E docker-compose -f ./development/docker-compose-dev.yml down -v

.PHONY: dev-build dev-start dev-down
