all: lint unit

dependencies:
	@pip install -U pip
	@pip install pipenv
	@pipenv install --dev --skip-lock

test:
	@make lint
	@make unit

lint:
	@echo "Checking code style ..."
	@pipenv run flake8 glassfrog tests

unit:
	@echo "Running unit tests ..."
	@pipenv run nosetests --with-coverage

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; done
	@echo "OK!"
	@printf "Deleting dist files"
	@rm -rf dist

release: lint unit
	@rm -rf dist/*
	@make rogue-release

rogue-release:
	@./.release
	@make pypi

pypi:
	@pipenv run python setup.py build sdist
	@pipenv run twine upload dist/*.tar.gz


.PHONY: lint pypi  clean unit test dependencies all