check: clean
	flake8 .
	radon cc --min B .
	radon mi --min B .

clean:
	autopep8 --in-place --recursive .

run:
	env $$(cat .env | xargs) python main.py

test:
	pytest tests
