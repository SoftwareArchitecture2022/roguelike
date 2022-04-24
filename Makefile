install:
	pip3 install llist pynput

test_unit: install
	python3 -m src.tests.unit-tests.run_tests
