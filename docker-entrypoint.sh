#!bin/sh

flask db upgrate

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"