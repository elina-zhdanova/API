.PHONY: install migrate run test

install:
	pip install -r requirements.txt

migrate:
	flask db upgrade

run:
	flask run

test:
	pytest -v

create-user:
	flask create-user $(username) $(password)