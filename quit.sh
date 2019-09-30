#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

function kill_pid_file() {
	local pid_file="$1"

	if [ -f "${pid_file}" ]; then
		for pid in `cat "${pid_file}"` ; do
			kill $pid
			echo > "${pid_file}"
		done
	else
		echo "No pidfile found"
		exit 1
	fi
}

pushd $(dirname $0) &> /dev/null

case $1 in
	server)
		kill_pid_file "server.pid"
		;;
	client)
		kill_pid_file "client.pid"
		;;
	*)
		kill_pid_file "server.pid"
		kill_pid_file "client.pid"
		;;
esac

popd &> /dev/null
