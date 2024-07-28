FROM grey.ctf/evm-infra

COPY ./contracts /tmp/contracts
COPY ./foundry.toml /tmp/foundry.toml

ENV PORT 33325
ENV HTTP_PORT 33326
ENV PUBLIC_IP "challs.nusgreyhats.org"
ENV FLAG "grey{e12c68229b1c9fe79072621d2ee0db31}"
ENV RPC_KILL_TIMEOUT 3600
