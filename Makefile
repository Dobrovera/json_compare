install: #установить зависимости
	poetry install
brain-games: #запуск gendiff
	poetry run gendiff
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install --user dist/*.whl
gendiff:
	poetry run python -m gendiff.scripts.gendiff --
