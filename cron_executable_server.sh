#!/bin/bash
PATH=/home/ubuntu/anaconda3/bin:/home/ubuntu/bin:/home/ubuntu/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:sbin:/bin


if ! pgrep gunicorn >/dev/null
then
     cd /app
     echo "Starting servers"
     bash start.sh
     ps -ef
     echo ""
fi