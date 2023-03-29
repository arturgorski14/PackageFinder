# PackageFinder
- short project description

## How to run
LOCAL:
- python manage.py runserver

DOCKER:
- docker-compose up --build  # build containers specified in docker-compose.yml
- docker-compose run --rm api sh -c "python manage.py search_index --rebuild"  # rebuild elastic index

## Tech Stack
- frameworks, libraries and why
