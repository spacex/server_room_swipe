#!/usr/bin/env bash

pushd $(dirname $0) &> /dev/null

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

export FLASK_APP=server_room_swipe.py
echo "#############################################################################"
echo "Starting flask, badge reader will come up in ~30seconds"
echo "#############################################################################"
flask run --port=80 --host=0.0.0.0 &
flask_pid=$!
echo "Started flask on PID: $flask_pid"

sleep 30
# the badge reader tries to immediately get a token
# which won't work until the server gets fully up (~30s)
echo "Starting badge reader"
python pi_client.py &> server.log &
pi_client_pid=$!
echo "Started badge reader on PID: $pi_client_pid"

echo $pi_client_pid >server_room_swipe.pids
echo $flask_pid >>server_room_swipe.pids

popd &> /dev/null
