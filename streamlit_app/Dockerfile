FROM ubuntu:22.04

RUN apt update
RUN apt install -y \
    python3 \
    python3-pip

RUN mkdir /app
ADD requirements.txt /app/
COPY ./src /app/src

WORKDIR /app/
RUN pip install -r requirements.txt

CMD ["streamlit", "run", "/app/src/app.py", "--server.port", "80"]