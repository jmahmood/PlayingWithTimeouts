web: GUNICORN_CMD_ARGS="--log-level=debug --graceful-timeout 20" env PYTHONPATH=$PYTHONPATH:$PWD/app newrelic-admin run-program gunicorn -k tornado server:app --log-file -
