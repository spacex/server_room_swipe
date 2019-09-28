#!/usr/bin/env bash

pushd $(dirname $0) &> /dev/null

rm -f app.db
rm -rf migrations

flask db init
flask db migrate
flask db upgrade
python drop_create_pi_account.py

popd &> /dev/null
