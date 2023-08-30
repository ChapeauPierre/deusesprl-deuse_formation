FROM python:3.10-bullseye

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# pip install
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install node for npm packages
ENV NODE_VERSION 16.14.0
ENV NVM_DIR /usr/local/.nvm
RUN mkdir -p $NVM_DIR
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version

# Install gettext (I18N)
RUN apt update
RUN apt-get install -y gettext

# create unprivileged user (celery)
RUN adduser --disabled-password --gecos '' myuser
