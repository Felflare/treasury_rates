FROM tiangolo/meinheld-gunicorn:python3.7

COPY app /app/app
COPY cron_executable_data.sh /app
COPY cron_executable_server.sh /app
COPY gunicorn_log.conf /app
COPY gunicorn_conf.py /app
COPY start.sh /app
COPY requirements.txt /app


ENV VARIABLE_NAME="server"
ENV MODULE_NAME="app.main"
ENV LOG_CONFIG_FILE="/app/gunicorn_log.conf"

RUN apt-get update && apt-get install -y cron

RUN pip install -r requirements.txt
RUN printenv | sed 's/^\(.*\)$/export \1/g' > /project_env.sh

# Copy hello-cron file to the cron.d directory
COPY cron_task /etc/cron.d/cron_task

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron_task
RUN chmod 0744 -R /app/

# Apply cron job
RUN crontab /etc/cron.d/cron_task

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

EXPOSE 80

# Run the command on container startup
CMD ["cron", "-f"]