# Base Django project template

This template should be used when a team considers using Django in one of their projects.

## Installation

For an installation procedure please refer to the file [README_install_base_project.md](README_install_base_project.md).

## Architecture

We opted for a Docker architecture which makes it easier to share projects between team members.

To install a project you can run the command `./install_docker.sh`. This command will pull and build the docker containers, then setup the database and initialise default user information. This makes it easy for team members to share their projects with other team members.

Once the containers run on your computer you can restore production databases locally by running the commands : `./google_storage.sh -a`, `./google_storage.sh -l` and `./google_storage.sh -r gs:...`. You can create a backup using the command `./google_storage.sh -b`.

We have three different environments:
- **LOCAL**, with the configuration of the dockers located in `docker-compose.yml`.
- **DEV**, which is in fact quality, with the configuration located in `dev.yml`.
- **PROD**, the production environment, with the configuration located in `prod.yml`.

We can add an entry in `/etc/host` in which we add the project name which points to `127.0.0.1`, e.g.: we can point `deuse.local` to `localhost` and our nginx **proxy-pass** will do the routing to web. Note, that you need to have the [DEUSE proxy pass](git@bitbucket.org:deusesprl/proxy_pass.git) installed and running on your machine.

You can stop a project by running the command `docker-compose stop`, you can start a project by running `docker-compose up -d`, to stop a specific container you can do `docker-compose stop web` and to start this container again but to view the output of the container in a console you can restart it with the command `docker-compose run web`. You can also restart all the containers by running `docker-compose restart`.

### Web server

We opted for a NGINX web server since it is the default for Django. All the configurations for our NGINX can be found in the folder `~/nginx/`. This folder is used to generate the NGINX docker container.

### The Django application

In the `~/web/` folder, we have all files related to the Django application. As a Software Engineer this is were you should add the most code. This folder is linked to the web container which runs our application.

#### NPM watch and frontend folder

In the `~/web/` folder we have a `frontend/` folder which contains the sass/js/react part of the project, if the project has one. It is linked to the `npm_watch` containers which only runs locally and watches for file changes to rebuild the frontend files.

### CRON

We also have a CRON container which may contain all the crons of our project including the backup system. The CRON container volumes are located in `~/cron/`.

Template file:

```sh
#!/bin/sh
CONTAINER_NAME=$(docker inspect -f '{{ .Name }}' "$HOSTNAME" | cut -c 2- | rev | cut -c 8- | rev)
CONTAINER_WEB_NAME=$(docker ps --format "{{.Names}}" | grep $CONTAINER_NAME | grep $CONTAINER_WEB | head -1)

# Run the command that <TASK_DESCRIPTION>
/usr/bin/flock -n /tmp/TASK_NAME.lockfile docker exec -u 1000:1000 -i "$CONTAINER_WEB_NAME" /usr/local/bin/python manage.py TASK_NAME
```
NB: Replace `TASK_DESCRIPTION` and `TASK_NAME` values.

#### Backup system

The backup system is located in the CRON container and runs every night around 3 a.m. Backups are located in Google Cloud storage.

You can use the backup system on your device with the following commands:
- `./google_storage.sh - a`, to authenticate your device on Google storage.
- `./google_storage.sh -l`, to list all existing remote backups in the Google storage.
- `./google_storage.sh -r gs:...`, to restore a specific backup url.
- `./google_storage.sh -b`, to backup your local instance.

### Celery & Flower

Since Django is a web framework and since it uses the HTTP standards if we run a task which has a duration longer than the NGINX connection timeout time then we get an error. To avoid this we use Celery as background task manager, Django sends long taks to Celery which executes them in the background. Flower is a web dashboard to check the progress off every task.

### Postgres

We use PostgreSQL as the default database technology for our Django projects.
