FROM grey.ctf/evm-infra

COPY ./contracts /tmp/contracts
COPY ./foundry.toml /tmp/foundry.toml

ENV PORT 33321
ENV HTTP_PORT 33322
ENV PUBLIC_IP "challs.nusgreyhats.org"
ENV FLAG "grey{fc901c94fb86106c322b94f5cec84fe5}"
ENV RPC_KILL_TIMEOUT 3600
