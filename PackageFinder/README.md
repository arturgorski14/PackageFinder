# PackageFinder
- short project description

## How to run
LOCAL:
- python manage.py runserver

DOCKER:

Set variable for docker desktop

In PowerShell
- wsl -d docker-desktop -u root
- vi /etc/sysctl.conf
In sysctl.conf file
- vm.max_map_count=262144

open Docker Desktop

From terminal
- docker-compose up
- docker-compose run --rm api sh -c "python manage.py search_index --rebuild"  # rebuild elastic index

## Tech Stack
- frameworks, libraries and why
