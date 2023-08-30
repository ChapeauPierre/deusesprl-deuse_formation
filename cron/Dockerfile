FROM alpine:3.13

# Install Docker to allow this container to run Docker commands
RUN apk add --update --no-cache docker
RUN apk update
RUN apk add py3-pip python3-dev libffi-dev openssl-dev gcc libc-dev make musl-dev cargo
RUN pip install --upgrade pip
RUN pip install docker-compose==1.24.0

# Copy the cronjobs
COPY tasks/ /etc/periodic/
RUN chmod -R +x /etc/periodic/

# Copy the logrotate configuration file
COPY logrotate/ /etc/logrotate.d/

# Add cron periods
RUN crontab -l | { cat; echo "*      *      *      *      * run-parts /etc/periodic/once_a_minute"; } | crontab -

# Runs the crond daemon in the foreground (so the container doesn't exit right away) and puts out
# the logs to stderr (so the output of the scheduled tasks can be seen using docker logs)
CMD ["crond", "-f", "-d", "8"]
