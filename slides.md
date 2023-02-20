---
author: Josh Brown
---
# Notes on projects
## Folder Structure

- Nested base project folders should have purpose.
- If your project has separate services (for example, an api that is separate from the UI), then each service should live in a subfolder labeled appropriately. 
- If your project is one service, no need to nest the project recursively. 
- Ex. ~/github/myproject vs ~/github/myproject/myproject

## .gitignore
- Look up .gitignore templates for your project
- Anything that changes during build / runtime generally should be ignored
- Anything that can be installed during setup should be ignored

- Common examples
    - `node_modules`
    - `__pycache__`
    - `.env`
    - `build/`
    - `dist/`

- Use a `sample.env` or `.env.sample` that IS stored in git, without secrets, and with reasonable defaults

*Note: these will generally also apply to .dockerignore*

---
# Notes on projects
## Branches
- Decide on a branching strategy
- I personally recommend the `github` flow for most teams
- A branch is not your branch
- Establishing naming patterns for your team can help a lot
- Writing down issues on gh can also help with this
    - Ex. for Brunus projects, we use the convention `[type]/[issue #]-[desc]`

## Comment on CRA

**Stop using Create React App, And get off of it, if you can**

### Why?
- Very slow, compared to newer alternatives
- Massive footprint
- Outdated and insecure
- Does not play well with plugins (TS, Tailwind, etc.)

### Alternatives

Are you making a SPA?
- Vite
- Nx

Want SSR / non SPA?
- Next.js
- Remix.js
- Astro (can be non-react too)

---
# What is docker?

- Docker is an open source software platform that allows you to build, test, and deploy applications quickly
- Docker uses tiny containers that are virtualised on the OS level
- Uses linux VM's (unless containers are running on linux) to run each container

# Before Docker
- Hypervisors
    - Resource Hungry
    - Full OS
    - Slow startup time
    - Can run multiple OS's simultaneously
``` 
```
- Bare metal
    - Polluted environment
    - Dependency management nightmare
    - "Works on my computer!"

---
# Docker to the rescue
- Programmatically define how images should be created via Dockerfile
- Can be easily managed via compose, kubernetes (not so easy), fargate, etc.
- Can be used on all OS's 
    - Fastest on linux
- Speed up development 10x

---
# The Dockerfile

An Nginx Example
```Dockerfile
# Defines the base image
FROM nginx:alpine 

# Sets the base directory for the container
# Essentially setting $HOME. This is up to you,
# Good defaults are `app`, or `bot`, etc.
WORKDIR /app

# Since we have set WORKDIR, `./` and `.` now refernce `/app`
# Copy takes the first n-1 arugemnts as filepaths relative to the 
# Project directory on your computer, and copies them into the docker
# image to the specified location, being the last paramater.
COPY ./site ./site

# Here, we are copying our projects `./nginx.conf` to the images
# `/etc/nginx/nginx.conf`
COPY ./nginx.conf /etc/nginx/nginx.conf 

# Normally, we would specify either `CMD` or `ENTRYPOINT`. Since we leave it blank,
# We are using the default nginx image's entrypoint, being to start nginx.

```

---
# The Dockerfile

A Flask Example
```Dockerfile
# Here, we use `as base` so we can reference this image later on.
FROM python:3.10-bullseye as base
WORKDIR /app

# Here, we are copying `Pipfile` and `Pipfile.lock` to `/app`
COPY Pipfile Pipfile.lock /app

# We can use RUN to do build time steps, such as updating packages,
# building or compiling src files, etc.
RUN apt-get update && apt-get -y install cron && rm -rf /var/lib/apt/lists/*

# Here we can use it to set the timezone:
RUN apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

# Here we can install the pipenv and all required packages during image build time
RUN python -m pip install --no-cache --upgrade pip pipenv
RUN pipenv lock && pipenv --clear && pipenv --rm
RUN pipenv install --deploy --system

# Copy all base files that are not listed in .dockerignore to /app
COPY . /app

# Here, we define our actual targets.

# `dev` is for dev mode, where when we start our container,
# it will start app.py, using werkzeug
FROM base as dev
CMD ["python", "-u", "app.py"]

# When we target prod, we will run prod.py, using waitress, a production ready http server
FROM base as prod
CMD ["python", "-u", "prod.py"]
```

---
# The Dockerfile
- Docker is very good at caching
- Each step in your Dockerfile should be in order of least expected change
- Copy dependencies over before source
- By default, docker will use the last target if none is specified
    - We can specify target in docker-compose or the docker cli

## Pitfalls
- Don't use multiple Dockerfiles, just use multiple build targets!
- Docker images are meant to be as light as possible.
    - Only copy what you need!
- Generally, if its in your `.gitignore`, it should be in your `.dockerignore`
    - `.dockerignore` should also contain entries for files such as `README.md`,
    `docker-compose.yml`, `.git`, etc.
- Make sure to watch the order of your build steps
```

```
For a much more complex dockerfile for node, see fullstack-app's Dockerfile

---
# Docker CLI
- I literally don't use it.
- Even with one container, I personally find docker-compose much easier

# Docker Compose
- Essentially docker cli commands written out in a .yml file
    - YAML is basically json if json was made by python
- Still use the cli to control docker-compose
- docker-compose controls the specifics of the containers
- docker-compose cli controls starting, stopping, restarting, etc. of containers

# Quick Terminology
- Docker
  - The ecosystem as a whole, all parts of docker.
- Image
  - The immutable template that defines how a container will start
- Container
  - An actual instance of an image
- Volume
  - A mapped file space for a container to use

---
# Docker Compose

docker-compose.yml for `simple-nginx`
```yml
# Just use version 3. Always specify this at the beginning of the file
version: "3"

# List of containers
services:

  # Our first (and only) container
  nginx:

    # What ports to map
    # "host:container"
    ports:
      - "80:80"

    # Options for building the image
    build:
      context: .

    # Mount our local ./site to /app/site
    # This lets us see changes we make to our local
    # filesystem immediatly in our image
    # Most configs like this are "host:container"
    volumes:
      - ./site:/app/site
```

---
# Docker Compose

docker-compose.yml for `flask-app`

```yml
version: "3"
services:
  app:
    build:
      context: .
      # Notice here, we specify which target
      target: dev
    ports:
      - '80:5000'

    # Here, we map our full workspace to inside the container
    volumes:
      - .:/app

    # This automatically loads our .env file into the container
    # so that we dont need to call any sort of "loadenv"
    env_file:
      - .env
```

---
# Docker Compose

docker-compose-prod.yml for `flask-app`

```yml
version: "3"
services:
  app:
    build:
      context: .
      target: prod
    ports:
      - '80:8080'

    # This tells the container it should always restart unless it is told to stop
    # if the host computer is restarted, the container will automatically start when
    # the host is done starting up
    restart: unless-stopped

    env_file:
      - .env
```
---

# Docker Compose

Lets look at a more complex version of a Dockerfile and docker-compose.yml

---
# Just? yeah we get it.

Justfile for `fullstack-app`, but a good baseline for most compose projects.
```make
# List defaults
default:
    @just --list

# Build images
build:
    @docker compose build

# Start containers
up: build
    @docker compose up -d

# Shutdown containers
down:
    @docker compose down

# Runs all tests
test: build
    @docker compose run app yarn lint

# Watch logs
logs:
    @docker compose logs -f
```

---

# Docker Compose

## The compose network

When compose starts containers, it will automatically create a network for all the containers to live in.
If your container uses ports, but they are not specified in the dockerfile or docker-compose file, they will
not be accessible.

Each container will automatically be assigned a DNS name according to its name in the compose file.
For example, see `fullstack-apps` networking

## Depends on

When composing a more complex project, sometimes containers need other containers to be ready before they
connect. This is solved with the `depends_on` field.

First, we add a `healthcheck` to a container. For a postgres instance, we could use
```yml
healthcheck:
  # Command to run inside the container
  test: pg_isready -d ${POSTGRES_DB} -U ${POSTGRES_USER}
  # how often to check
  interval: 10s
  # how long before a failure should be assumed for a given attempt
  timeout: 5s
  # how many retries before service is declared unhealthy
  retries: 10
```

Next, we add a `depends_on` field to our service that depends on our aforementioned container
```yml
depends_on:
  db:
    condition: service_healthy
```
Now, our second service will wait until our database is ready before initializing. 


---
# Docker Compose

## Volumes

Named volumes, as seen in `fullstack-app` let us easily define reusable, out-of-container
data. We hook into our volumes with a `volumes` directive
```yml
volumes:
  - pgdata:/var/lib/postgresql/data
```
Then, we can define a volume at the end of our docker-compose file
```yml
volumes:
  pgdata:
```

Note, that defined volumes do not start with `./`. If we defined the volume in the container section as
```yml
volumes:
  - ./pgdata:/var/lib/postgresql/data
```
Then a folder in our project would be created, and the data would be kept there


### Pitfall
If docker has to create files in a mounted volume, then the files will be created as root! This can be troublesome depending on
the project. The best idea is to keep volumes that docker manages (like postgres data) in a named volume, and user managed Volumes
(like source code) as mapped.


---
# Docker Compose

- Dev containers vs Production
    - Dev
        - Mapping src
        - Ports
    - Prod
        - May only need a docker-compose.yml file, no sourcecode needed.
        - Might use different host ports
