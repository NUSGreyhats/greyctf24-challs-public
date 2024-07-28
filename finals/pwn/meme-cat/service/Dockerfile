# source filesystem
FROM ubuntu:22.04 AS app
# apt install any dependencies if necessary
RUN apt-get update && rm -rf /var/lib/apt/lists/* 

# this is the actual container that runs
FROM pwn.red/jail
# copy ubuntu file system into our redpwn jail
COPY --from=app / /srv
# copy local file into docker
COPY ./challenge /srv/app/run
COPY ./ld-2.31.so /srv/app/ld-2.31.so
COPY ./libc.so.6 /srv/app/libc.so.6
# copy flag into docker if needed
COPY ./flag.txt /srv/app/flag.txt

