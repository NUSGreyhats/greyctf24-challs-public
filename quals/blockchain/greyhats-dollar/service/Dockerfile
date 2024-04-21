FROM grey.ctf/evm-infra

COPY ./contracts /tmp/contracts
COPY ./foundry.toml /tmp/foundry.toml

ENV PORT 30201
ENV HTTP_PORT 30202
ENV PUBLIC_IP "challs.nusgreyhats.org"
ENV FLAG "grey{self_transfer_go_brrr_9e8284917b42282d}"
ENV RPC_KILL_TIMEOUT 3600
