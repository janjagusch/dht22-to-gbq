@PHONY: format_black
format_black:
	black dht_to_gbq

@PHONY: lint_black
lint_black:
	black --check dht_to_gbq

@PHONY: lint_pylint
lint_pylint:
	pylint dht_to_gbq

@PHONY: lint
lint:
	make lint_black
	make lint_pylint
