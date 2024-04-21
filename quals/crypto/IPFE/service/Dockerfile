# greyctf pwn jail
## Based on https://github.com/redpwn/jail
# Rudimentary per-connection python runner based on the Pwn Dockerfile template

FROM python:3.11 AS src

RUN apt-get update
RUN apt-get install -y libgmp-dev libmpfr-dev libmpc-dev
RUN pip install --no-cache-dir gmpy2
RUN pip install --no-cache-dir pycryptodome

# This is the actual container that runs
FROM redpwn/jail:latest

ENV JAIL_TIME 300
ENV JAIL_CPU 0
ENV JAIL_MEM 0

# Copy the entire python filesystem from src to here
COPY --from=src / /srv/
COPY ./server.py /srv/app/run
COPY ./IPFE.py /srv/app/IPFE.py
EXPOSE 5000
RUN chmod +x /srv/app/run
RUN chmod +x /srv/app/IPFE.py