# PackageFinder
- Simple Django App that utilizes Elasticsearch to find and filter results.
- Every 24h runs cron which updates Elasticsearch index "packages".

## Before first run
### Set variable for docker desktop - elasticsearch won't work otherwise
Open PowerShell and type following commands:
- wsl -d docker-desktop -u root
- vi /etc/sysctl.conf
Then add following line in sysctl.conf file
- vm.max_map_count=262144

PAGINATE_BY:
- sets how many results are displayed on single page,
- default value is 25,
- changeable in Dockerfile.

## How to run
- docker-compose up -d
- go to http://localhost:8000/fill in order to populate elasticsearch on demand

## Additional info
### elasticsearch data is stored in volume
- \\wsl$\docker-desktop-data\data\docker\volumes

