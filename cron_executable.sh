#!/bin/bash
PATH=/home/ubuntu/anaconda3/bin:/home/ubuntu/bin:/home/ubuntu/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:sbin:/bin



cd app/data_pull
python pull_data.py
python process_csv.py

killall gunicorn
sleep 30
cd /app
bash start.sh