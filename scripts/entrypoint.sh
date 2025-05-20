#!/bin/sh

set -e
# start cron
echo "Contenedor iniciado"
/usr/sbin/crond -f -l 8
echo "crond iniciado"
