#!/bin/bash

GUNICORN_CMD_ARGS="--bind=127.0.0.1:9999 --workers=3 --log-level=warning --graceful-timeout 30" gunicorn -k tornado server:app &
BACKGROUND_SERVER_PID=$!

GUNICORN_CMD_ARGS="--bind=127.0.0.1:8000 --workers=3 --log-level=debug --graceful-timeout 20" gunicorn -k tornado server:app &
FOREGROUND_SERVER_PID=$!

sleep 5s

# This should serve normally.
/usr/bin/curl -s http://127.0.0.1:8000/remote/1 > /dev/null &

# This should return normally after it is killed.
/usr/bin/curl  -s -D - http://127.0.0.1:8000/remote/10 -o /dev/null &

sleep 2s

# The foreground parent process should be killed; any request to this url should be ignored and not logged.
kill $FOREGROUND_SERVER_PID
sleep 2s

# This should not be received!  It should not show up in the log as it happened after the sigterm.
/usr/bin/curl  -s -D - http://127.0.0.1:8000/remote/20  -o /dev/null

# Once all the excitement is done, kill the silent background server.
kill $BACKGROUND_SERVER_PID
