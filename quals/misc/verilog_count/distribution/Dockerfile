FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y \
    python3 \
    socat \
    iverilog 

RUN mkdir /app

COPY run.py /
COPY run.sh /
COPY expected_output.txt /
COPY test /test

RUN chmod 555 /run.py
RUN chmod 555 /run.sh
RUN chmod -R 555 /test
RUN chmod 555 expected_output.txt

CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:/run.sh,stderr
