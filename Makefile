install:
	pip install -r requirements.txt
lint:
	pylint --disable=R,C *.py
format:
	black *.py