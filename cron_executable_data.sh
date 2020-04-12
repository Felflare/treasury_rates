#!/bin/bash
PATH=/home/ubuntu/anaconda3/bin:/home/ubuntu/bin:/home/ubuntu/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:sbin:/bin


date
cd /app/app/data_pull
python pull_data.py
python process_csv.py
echo "Stopping old servers"
killall gunicorn
echo ""