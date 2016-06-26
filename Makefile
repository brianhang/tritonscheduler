init:
	pip install -r requirements.txt

test:
	python tests/test_classtime.py
	python tests/test_schedule.py
