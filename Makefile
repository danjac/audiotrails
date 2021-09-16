all: build migrate seed test start

build:
	docker-compose build

start:
	docker-compose up -d --remove-orphans --scale worker=4

stop:
	docker-compose down

restart:
	docker-compose restart

migrate:
	./bin/manage migrate

superuser:
	./bin/manage createsuperuser

seed:
	./bin/manage seed_podcast_data

shell:
	./bin/manage shell_plus

test:
	./bin/runtests -v -x --ff --reuse-db

coverage:
	./bin/runtests -v -x --cov --reuse-db

upgrade:
	./bin/poetry update -vv
	./bin/poetry export -o requirements.txt  --without-hashes
	./bin/npm update

maint: maintenance

maintenance:
	ansible-playbook maintenance.yml --ask-pass

requirements:
	./bin/poetry export -o requirements.txt  --without-hashes

push:
	git push dokku main
