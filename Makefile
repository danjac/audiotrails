build: install nltk

install:
	python -m pip install -r requirements/dev.txt
	npm ci
	pre-commit install

nltk:
	xargs python -m nltk.downloader <./nltk.txt

test:
	python -m pytest

db:
	python ./manage.py migrate
	python ./manage.py loaddata ./radiofeed/podcasts/fixtures/categories.json.gz
	python ./manage.py loaddata ./radiofeed/podcasts/fixtures/podcasts.json.gz

clean:
	git clean -Xdf

update:
	pip-compile --upgrade requirements/prod.in -o requirements/prod.txt --resolver=backtracking
	pip-compile --upgrade requirements/ci.in -o requirements/ci.txt --resolver=backtracking
	pip-compile --upgrade requirements/dev.in -o requirements/dev.txt --resolver=backtracking
	python -m pip install -r requirements/dev.txt
	npm run check-updates && npm install
	pre-commit autoupdate
