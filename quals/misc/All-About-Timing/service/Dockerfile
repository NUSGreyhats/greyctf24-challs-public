FROM python:slim AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY ./time.py /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod +x /srv/app/run

ENV JAIL_MEM=0
ENV JAIL_CPU=0
