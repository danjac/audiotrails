install: pyinstall npminstall precommitinstall nltkdownload

dbinstall: migrate fixtures

update: pyupdate pyexport npmupdate precommitupdate

pyinstall:
	poetry env use 3.12
	poetry install --no-cache

pyupdate:
	poetry update --no-cache

pyexport:
	poetry export -o requirements.txt --without-hashes
	poetry export -o requirements-ci.txt --with=dev --without-hashes

npminstall:
	npm ci

npmupdate:
	npm run check-updates && npm install

precommitinstall:
	pre-commit install

precommitupdate:
	pre-commit autoupdate

nltkdownload:
	xargs -I{} python -c "import nltk; nltk.download('{}')" < nltk.txt

migrate:
	python ./manage.py migrate

fixtures:
	python ./manage.py loaddata ./radiofeed/podcasts/fixtures/categories.json.gz
	python ./manage.py loaddata ./radiofeed/podcasts/fixtures/podcasts.json.gz
	python ./manage.py loaddata ./radiofeed/users/fixtures/users.json.gz

serve:
	python ./manage.py runserver

shell:
	python ./manage.py shell_plus

build:
	npm run build

watch:
	npm run watch

test:
	python -m pytest

clean:
	git clean -Xdf
