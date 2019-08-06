.PHONY: test
test:
	pipenv run pytest


.PHONY: ci
ci:
	pipenv run pytest # --cov=fast_arrow tests/


.PHONY: pc
pc: l test


.PHONY: lint
lint:
	pipenv run flake8 --exclude fast_arrow_auth/__init__.py,examples/*,build/*,setup.py,.tox/*


.PHONY: examples
examples:
	pipenv run run_all_examples
