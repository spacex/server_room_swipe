#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi
cd /home/pi/server_room_swipe
echo "Starting badge reader"
python pi_client.py &
pi_client_pid=$!
echo "Started badge reader on PID: $pi_client_pid"

export FLASK_APP=server_room_swipe.py
echo "#############################################################################"
echo "Starting flask, wait for \"Running on http://...\" before scanning any badges"
echo "#############################################################################"
flask run --port=80 --host=0.0.0.0 &
flask_pid=$!
echo "Started flask on PID: $flask_pid"

echo $pi_client_pid >server_room_swipe.pids
echo $flask_pid >>server_room_swipe.pids
