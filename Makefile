.PHONY: dev
dev:
	uv run appleconnector

.PHONY: clean
clean:
	rm -rf build dist *.egg-info

.PHONY: install
install:
	uv sync

.PHONY: publish
publish: clean
	uv build
	uv run twine upload --username __token__ dist/*

.PHONY: lint
lint: ## run lint
	uv run black appleconnector
	uv run flake8 appleconnector
	uv run pylint $$(git ls-files '*.py' | grep -v 'docs/conf.py') --rcfile=./pylintrc