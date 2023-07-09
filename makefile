
install:
	conda create -p env python=3.10 -y
	env/bin/python -m pip install -r requirements.txt -e .

format:
	env/bin/python -m black gobblers

test: format
	env/bin/python -m pytest -vv gobblers/test_*.py
