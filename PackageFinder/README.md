# PackageFinder
- Simple Django App that utilizes Elasticsearch to find and filter results.
- Every 24h runs cron which updates Elasticsearch index "packages".

## Before first run
### Set variable for docker desktop - elasticsearch won't work otherwise
In PowerShell
- wsl -d docker-desktop -u root
- vi /etc/sysctl.conf
Then in sysctl.conf file
- vm.max_map_count=262144

inside project's Dockerfile set PAGINATE_BY to change how many results are displayed on single page

## How to run
- docker-compose up -d
- go to http://localhost:8000/fill in order to populate elasticsearch on demand

## Additional info
### elasticsearch data is stored in volume
- \\wsl$\docker-desktop-data\data\docker\volumes

