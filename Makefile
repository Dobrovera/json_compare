install: #установить зависимости
	poetry install

build:
	poetry build

upgrage-pip:
	python3 -m pip install --upgrade pip

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
