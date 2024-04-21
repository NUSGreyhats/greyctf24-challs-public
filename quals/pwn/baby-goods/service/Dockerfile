# source filesystem
FROM ubuntu:22.04 AS app
FROM pwn.red/jail
COPY --from=app / /srv
# copy local file into docker
COPY ./babygoods /srv/app/run
COPY ./flag.txt /srv/app/flag.txt

RUN chmod 444 /srv/app/flag.txt
RUN chmod +x /srv/app/run

