FROM alpine:3.6

RUN apk add --update musl python py-pip bash gcc make ncurses-dev readline readline-dev libffi-dev py-cffi python-dev musl-dev && \
    rm /var/cache/apk/*

#RUN apk add --no-cache gcc python3-dev musl curl

RUN pip install falcon gunicorn


RUN apk upgrade --no-cache


COPY ./requirements.txt /tmp
RUN pip install --proxy=10.0.0.1:3128 -r /tmp/requirements.txt

EXPOSE 8002
COPY ./app /app

WORKDIR /app
CMD ["gunicorn", "-b", "0.0.0.0:8002", "-w", "4", "app:api"]