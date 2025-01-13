.PHONY: dev
dev:
	pipenv run appleconnector

.PHONY: clean
clean:
	rm -rf build dist *.egg-info

.PHONY: publish
publish: clean
	pipenv run python setup.py sdist bdist_wheel
	twine upload --username mre0 dist/*

.PHONY: lint
lint: ## run lint
	pipenv run black appleconnector
	pipenv run flake8 appleconnector
	pipenv run pylint $$(git ls-files '*.py' | grep -v 'docs/conf.py') --rcfile=./pylintrc