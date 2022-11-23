install: #установить зависимости
	poetry install
gendiff: #запуск gendiff
	poetry run gendiff
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install --user dist/*.whl
gendiff:
	poetry run python -m gendiff.scripts.gendiff --
lint:
    poetry run flake8 gendiff