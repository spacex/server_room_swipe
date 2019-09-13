rm -f ~/server_room_swipe/app.db
rm -rf ~/server_room_swipe/migrations

flask db init
flask db migrate
flask db upgrade
python drop_and_dane.py
