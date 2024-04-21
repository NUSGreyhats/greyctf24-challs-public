FROM python:slim AS app

RUN python3 -m pip install numpy

FROM pwn.red/jail
COPY --from=app / /srv
COPY ./poly.py /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod +x /srv/app/run

ENV JAIL_MEM=0
ENV JAIL_CPU=0
ENV JAIL_TIME=60
