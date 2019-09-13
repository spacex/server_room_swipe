#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

cd /home/pi/server_room_swipe
export FLASK_APP=server_room_swipe.py

flask run --port=80 --host=0.0.0.0 &
python pi_client.py &

