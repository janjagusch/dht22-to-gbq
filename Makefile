@PHONY: format_black
format_black:
	black .

@PHONY: lint_black
lint_black:
	black --check .

@PHONY: lint_pylint
lint_pylint:
	pylint main.py

@PHONY: lint
lint:
	make lint_black
	make lint_pylint
