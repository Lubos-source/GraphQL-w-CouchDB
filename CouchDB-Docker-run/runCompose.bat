set COMPOSE_CONVERT_WINDOWS_PATHS=1
docker-compose -p CouchDB_GQL up -d
pause
docker-compose -p CouchDB_GQL down