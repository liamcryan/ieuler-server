#!/bin/bash
while true; do
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done

exec gunicorn -b 0.0.0.0:2718 "app:create_app()"