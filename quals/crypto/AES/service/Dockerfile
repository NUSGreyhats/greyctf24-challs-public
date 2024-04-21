# greyctf pwn jail
## Based on https://github.com/redpwn/jail
# Rudimentary per-connection python runner based on the Pwn Dockerfile template

FROM python:3 AS src

# This is the actual container that runs
FROM redpwn/jail:latest

ENV JAIL_TIME 300
ENV JAIL_CPU 0
ENV JAIL_MEM 0

# Copy the entire python filesystem from src to here
COPY --from=src / /srv/
COPY ./server.py /srv/app/run
COPY ./aes.py /srv/app/aes.py
EXPOSE 5000
RUN chmod +x /srv/app/run
RUN chmod +x /srv/app/aes.py
