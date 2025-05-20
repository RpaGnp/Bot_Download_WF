#!/bin/sh

set -e

echo "$(date): Ejecutando proceso"
cd /app
# sudo pkill python
python app.py --windowed
# python Bot.py --windowed
echo "$(date): Fin del proceso"
