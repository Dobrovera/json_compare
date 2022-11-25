install: #установить зависимости
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user --force dist/*.whl

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest

pytest-cov:
	pip install pytest-cov

test-coverage:
	pytest --cov=gendiff
