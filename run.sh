#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

pushd $(dirname $0) &> /dev/null

case "$1" in
	server)
		export FLASK_APP=server_room_swipe.py
		echo "#############################################################################"
		echo "Starting flask, badge reader will come up in ~30seconds"
		echo "#############################################################################"
		flask run --port=80 --host=0.0.0.0 &> server.log &
		flask_pid=$!
		echo $flask_pid > server.pid

		# the badge reader tries to immediately get a token
		# which won't work until the server gets fully up (~30s)
		sleep 30

		echo "Started flask on PID: $flask_pid"
		;;
	client)
		echo "Starting badge reader"
		python pi_client.py &> client.log &
		pi_client_pid=$!
		echo $pi_client_pid > client.pid
		echo "Started badge reader on PID: $pi_client_pid"
		;;
	*)
		$0 server
		$0 client
		;;
esac

popd &> /dev/null
