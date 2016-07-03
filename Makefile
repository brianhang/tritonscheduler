init:
	pip install -r requirements.txt

test:
	python -m unittest tests/test_classtime.py
	python -m unittest tests/test_schedule.py

run:
	@python tritonscheduler/main.py
