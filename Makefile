SHELL=/bin/bash

clean:
	rm -rf build dist *.egg-info *.pyc

install:
	python setup.py install

test:
	cd tests && python ./test_poodledo.py

.PHONY: clean install test
