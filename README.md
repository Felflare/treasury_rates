# Yield Curve App
sudo docker build --rm -t treasury_rates ./
sudo docker run -d --name treasury_rates_cntr -p 8002:80 -v ~/treasury_rates/app/data_pull:/app/app/data_pull treasury_rates
  
============================ 
sudo docker rmi --force treasury_rates
sudo docker container rm --force treasury_rates_cntr

============================
sudo docker exec -it treasury_rates_cntr /bin/bash

============================
cat /var/log/cron.log

============================
env - `cat ~/cronenv` /bin/sh
