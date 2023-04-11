# netbox-object-storage
Plugin quản lý về object storage

## Installing
### For netbox Install using service systemd

To install the plugin, first using pip and install netbox-object-storage:

```
/opt/netbox/venv/bin/activate
pip3 install git+https://github.com/hocchudong/netbox-object-storage.git@main
```

Next, enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`, or if you have a `/configuration/plugins.py `file, the plugins.py file will take precedence.

```
PLUGINS = [
    'netbox_object_storage'
]
```

Migrate DB: 

```
python3 /root/netbox/netbox/manage.py migrate
```

Then you may need to perform the final step of restarting the service to ensure that the changes take effect correctly:

```
sudo systemctl restart netbox
```

## For netbox Install using docker
**Step-1**: Prepare 

- Clone netbox project

```
git clone -b release https://github.com/netbox-community/netbox-docker.git

cd netbox-docker
```

- Create a few files these are (`plugin_requirements.txt`, `Dockerfile-Plugins`, `docker-compose.override.yml`)


**Step-2**: File `plugin_requirements.txt` using for declare plugin or pip requirement with the following content:

```
gunicorn
git+https://github.com/hocchudong/netbox-object-storage.git@main
```

**Step-3**: File `Dockerfile-Plugins` will enable to build a new image with the required plugins:

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

**Step-4**: File `docker-compose.override.yml` to configuration overrides for existing services or entirely new services of netbox:

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

**Step-5**: Build and run docker-compose

```
docker-compose build --no-cache
docker-compose up -d
```

