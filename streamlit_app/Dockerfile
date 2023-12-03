FROM ubuntu:22.04

RUN apt update
RUN apt install -y \
    python3 \
    python3-pip \
    gettext

RUN mkdir /app
ADD requirements.txt /app/
COPY ./src /app/src

WORKDIR /app/
RUN pip install -r requirements.txt

RUN find /app/src -type f -name "*.mo" -delete
RUN find /app/src -type f -name "*.po" -execdir bash -c 'msgfmt {} -o "$(basename {} .po).mo"' \;

CMD ["streamlit", "run", "/app/src/app.py", "--server.port", "80"]