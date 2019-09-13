#!/usr/bin/env bash

cd /home/pi/server_room_swipe
export FLASK_APP=server_room_swipe.py

flask run --host=0.0.0.0 &
python pi_client.py &

