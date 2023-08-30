#!/bin/bash

PROJECT_NAME=archive
REPO=`git config --get remote.origin.url`

# First, Clone repository and remove the git folder
function check_files {
  echo -e "\n*** Please check some files ***"
  echo -e "\nEMAIL_HOST_USER, EMAIL_HOST_PASSWORD into .env file"
  echo ""

  echo "Do you want to continue ?"
  read -p "(y/N) ? " choice
  case "$choice" in
    y|Y )
      echo "We will create the zip file..."
      ;;
    * )
      echo "Bye"
      exit 1
  esac

  echo "[DONE]"
}

# First, Clone repository and remove the git folder
function get_repository {
  echo -e "\n*** Clone base_django_project repository ***"

  git clone $REPO $PROJECT_NAME
  cd $PROJECT_NAME
  git checkout master
  cd ..

  # rm -rf $PROJECT_NAME/ultrahook
  rm -rf $PROJECT_NAME/.git
  # rm -rf $PROJECT_NAME/docker-compose.yml
  rm -rf $PROJECT_NAME/dev.yml
  rm -rf $PROJECT_NAME/install_docker.sh
  rm -rf $PROJECT_NAME/create_archive.sh
  rm -rf $PROJECT_NAME/documentation.md
  rm -rf $PROJECT_NAME/README_install_base_project.md
  # rm -rf $PROJECT_NAME/nginx/Dockerfile
  # rm -rf $PROJECT_NAME/nginx/nginx-confs/local_nginx.conf
  rm -rf $PROJECT_NAME/nginx/Dockerfile-dev
  rm -rf $PROJECT_NAME/nginx/nginx-confs/local_nginx-dev.conf
  rm -rf $PROJECT_NAME/web/install_web.sh
  rm -rf $PROJECT_NAME/web/frontend.sh
  rm -rf $PROJECT_NAME/web/flush_logs.sh
  rm -rf $PROJECT_NAME/web/user/fixtures
  find $PROJECT_NAME -name ".gitignore" -exec rm -rf {} \;
  find $PROJECT_NAME -name ".gitkeep" -exec rm -rf {} \;

  sed -i '/deuse/d' $PROJECT_NAME/nginx/nginx-confs/.htpasswd

  echo "[DONE]"
}

# Add/Remove the google storage
function remove_google_storage {
  echo -e "\n*** Init google storage ***"

  echo "Do you want to remove your google-storage on this project ?"
  read -p "(Y/n) ? " choice
  case "$choice" in
    n|N )
      echo "Nothing to do"
      ;;
    * )
      echo "Remove backup system"
      rm -rf $PROJECT_NAME/cron/backup_system
      rm -rf $PROJECT_NAME/cron/logrotate
      sed -i '/backup/d' $PROJECT_NAME/cron/Dockerfile
      sed -i '/logrotate/d' $PROJECT_NAME/cron/Dockerfile
      sed -i '/Install Google Cloud/,/install.sh/d' $PROJECT_NAME/cron/Dockerfile

      rm -rf $PROJECT_NAME/google_storage.sh
      ;;
  esac

  echo "[DONE]"
}

# Copy local media folder
function copy_local_media {
  echo -e "\n*** Copy local media folder ***"

  echo "Do you want to copy local media folder ?"
  read -p "(Y/n) ? " choice
  case "$choice" in
    n|N )
      echo "Nothing to do"
      ;;
    * )
      echo "Copy local media folder"
      cp -r web/media/* $PROJECT_NAME/web/media/.
      ;;
  esac

  echo "[DONE]"
}

# Create dump from local DB
function create_dump {
  echo -e "\n*** Create dump from local DB ***"

  echo "Do you want to create SQL dump from local DB ?"
  read -p "(Y/n) ? " choice
  case "$choice" in
    n|N )
      echo "Nothing to do"
      ;;
    * )
      echo "Create dump from local DB"
      docker-compose up -d postgres
      docker-compose exec postgres pg_dumpall -c -U postgres > "$PROJECT_NAME"/`date +%Y-%m-%d"_"%H-%M-%S`_dump.sql
      ;;
  esac

  echo "[DONE]"
}

function write_docker_readmefile {
  echo -e "\n*** Create README_docker file ***"

  echo "How to build and run docker containers:" > "$PROJECT_NAME"/README_docker.txt
  echo "1. Build docker images: docker-compose -f docker-compose.yml build" >> "$PROJECT_NAME"/README_docker.txt
  echo "2. Start docker containers: docker-compose -f docker-compose.yml up -d" >> "$PROJECT_NAME"/README_docker.txt
  echo "3. Run web container scripts (not mandatory):" >> "$PROJECT_NAME"/README_docker.txt
  echo "  3.1 Apply migrations: docker-compose -f docker-compose.yml exec web ./manage.py migrate" >> "$PROJECT_NAME"/README_docker.txt
  echo "  3.2 Apply Npm install/build: docker-compose -f docker-compose.yml exec web /bin/bash -c 'cd frontend && npm install && npm run build'" >> "$PROJECT_NAME"/README_docker.txt
  echo "  3.3 Apply Collecstatic: docker-compose -f docker-compose.yml exec web ./manage.py collectstatic --noinput" >> "$PROJECT_NAME"/README_docker.txt
  echo "4. Restart everything: docker-compose -f docker-compose.yml stop && docker-compose -f docker-compose.yml up -d" >> "$PROJECT_NAME"/README_docker.txt
  echo "" >> "$PROJECT_NAME"/README_docker.txt
  echo "Production: Use prod.yml file => docker-compose -f prod.yml [...]" >> "$PROJECT_NAME"/README_docker.txt
  echo "" >> "$PROJECT_NAME"/README_docker.txt
  echo "DB: Restore backup" >> "$PROJECT_NAME"/README_docker.txt
  echo 'docker exec -t <NOM_DU_CONTAINER_POSTGRESQL> psql -U postgres -c "drop schema public cascade; create schema public AUTHORIZATION postgres;"'>> "$PROJECT_NAME"/README_docker.txt
  echo "cat <FICHIER_SQL> | docker exec -i <NOM_DU_CONTAINER_POSTGRESQL> psql -U postgres" >> "$PROJECT_NAME"/README_docker.txt

  echo "[DONE]"
}

# Create ZIP file
function create_zip {
  echo -e "\n*** Create ZIP file ***"

  zip -r $PROJECT_NAME.zip $PROJECT_NAME
  rm -rf $PROJECT_NAME

  echo "[DONE]"
}

check_files
get_repository
remove_google_storage
copy_local_media
create_dump
write_docker_readmefile
create_zip
