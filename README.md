Server Room Swipe
==========

# Installation
### Prerequisites
- python 2.7
- python-pip `apt install python-pip`
- flask-admin      `pip install flask-admin`
- flask-httpauth   `pip install flask-httpauth`
- flask-login      `pip install flask-login`
- flask-migigrate  `pip install flask-migrate`
- flask-sqlalchemy `pip install flask-sqlalchemy`
- flask-wtforms    `pip install flask-wtf`
- evdev            `pip install evdev`
- pytz             `pip install pytz`
- requests         `pip install requests`

### Steps
- `git clone https://github.com/lime45/server_room_swipe.git`
- `cd` into the repo
- `sudo ./run.sh |& tee server.log` to start the server
- `sudo ./quit.sh` to stop the server

## TODOs
- Use a real web server instead of the one that comes with Flask
- Make the UI less-ugly with CSS to make look and feel more consistent
