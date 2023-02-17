FROM python:3.10-bullseye as base

WORKDIR /app

COPY Pipfile Pipfile.lock /app

RUN apt-get update && apt-get -y install cron && rm -rf /var/lib/apt/lists/*
# Easy way to set timezone to wherever the docker image is running
RUN apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN python -m pip install --no-cache --upgrade pip pipenv
RUN pipenv lock && pipenv --clear && pipenv --rm
RUN pipenv install --deploy --system
COPY . /app

FROM base as dev
CMD ["python", "-u", "app.py"]

FROM base as prod
CMD ["python", "-u", "prod.py"]
