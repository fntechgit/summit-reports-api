#!/bin/bash
set -e
export DOCKER_SCAN_SUGGEST=false

docker compose run --rm app python manage.py migrate --database=openstack_db
docker compose up -d
docker compose exec app /bin/bash