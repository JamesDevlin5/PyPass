
SRC_FILE=password.py
RUNNER=python
FORMATTER=black

default:
	python $(SRC_FILE)

fmt:
	$(FORMATTER) $(SRC_FILE)

.PHONY: fmt

