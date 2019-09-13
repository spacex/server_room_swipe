#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi
cd /home/pi/server_room_swipe

if [ -f server_room_swipe.pids ]; then
	for pid in `cat server_room_swipe.pids` ; do
		kill $pid
	done
else
	echo "No pidfile found"
	exit 1
fi
