# Schools in Singapore

Simple app to search for schools in Singapore. Demonstrate using Python, Django,
React and ElasticSearch

## Requirement

- Python 3.6, pipenv
- NodeJS
- Docker

## Run each of these in one terminal tab

```sh
docker-compose up
```

```sh
npm install
npm start
```

```sh
pipenv install
pipenv run ./manage.py migrate
pipenv run ./manage.py createsuperuser
pipenv run ./manage.py import general-information-of-schools.csv
pipenv run ./manage.py search_index --create
pipenv run ./manage.py search_index --populate
pipenv run ./manage.py runserver
```

## TODO

- Properly handle keyword filters
- Dockerfile to build deployment image
