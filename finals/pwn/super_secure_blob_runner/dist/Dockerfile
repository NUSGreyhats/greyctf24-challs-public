FROM ubuntu@sha256:a6d2b38300ce017add71440577d5b0a90460d0e57fd7aec21dd0d1b0761bbfb2

ENV user ctf

RUN apt-get -y update
RUN apt-get install -y python3 socat && rm -rf /var/lib/apt/lists/*

RUN useradd $user
WORKDIR /home/$user

COPY ./chall /home/$user/chall
COPY ./run.py /home/$user/run.py
COPY ./flag.txt /home/$user/flag.txt
RUN chmod +x chall
RUN chmod +x run.py

CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:/home/$user/run.py,stderr
