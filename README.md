# netbox-object-storage
Plugin quản lý về object storage

## Installing

#### Step 1: Prepare 

- Clone netbox project

```
git clone -b release https://github.com/netbox-community/netbox-docker.git

cd netbox-docker
```

- Create a few files these are (`plugin_requirements.txt`, `Dockerfile-Plugins`, `docker-compose.override.yml`)


#### Step 2: File `plugin_requirements.txt` using for declare plugin or pip requirement with the following content:

```
gunicorn
git+https://github.com/hungviet99/netbox-object-storage.git@main
```

#### Step3: File `Dockerfile-Plugins` will enable to build a new image with the required plugins:

```
FROM netboxcommunity/netbox:latest

COPY ./plugin_requirements.txt /

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update -qq \
    && apt-get upgrade \
        --yes -qq --no-install-recommends \ 
    && apt-get install git -y

RUN /opt/netbox/venv/bin/pip install  --no-warn-script-location -r /plugin_requirements.txt

# These lines are only required if your plugin has its own static files.
COPY configuration/configuration.py /etc/netbox/config/configuration.py
RUN SECRET_KEY="dummy" /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py collectstatic --no-input
```

#### Step4: File `docker-compose.override.yml` to configuration overrides for existing services or entirely new services of netbox:

```
version: '3.4'
services:
  netbox:
    ports:
      - 8000:8080
    build:
      context: .
      dockerfile: Dockerfile-Plugins
    image: netbox:latest-plugins
  netbox-worker:
    image: netbox:latest-plugins
    build:
      context: .
      dockerfile: Dockerfile-Plugins
  netbox-housekeeping:
    image: netbox:latest-plugins
    build:
      context: .
      dockerfile: Dockerfile-Plugins
```

#### Step 5: Build and run docker-compose

```
docker-compose build --no-cache
docker-compose up -d
```

