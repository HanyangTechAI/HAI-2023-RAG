FROM python:3.10-slim as base

RUN apt update
RUN apt install -y gettext

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

FROM base

COPY ./src /app/src

RUN find /app/src -type f -name "*.mo" -delete
RUN find /app/src -type f -name "*.po" -execdir bash -c 'msgfmt {} -o "$(basename {} .po).mo"' \;

ARG STREAMLIT_SERVER_PORT
CMD ["streamlit", "run", "/app/src/app.py"]
