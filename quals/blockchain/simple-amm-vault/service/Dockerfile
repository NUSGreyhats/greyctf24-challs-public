FROM grey.ctf/evm-infra

COPY ./contracts /tmp/contracts
COPY ./foundry.toml /tmp/foundry.toml

ENV PORT 30301
ENV HTTP_PORT 30302
ENV PUBLIC_IP "challs.nusgreyhats.org"
ENV FLAG "grey{vault_reset_attack_a3e7a42b511cf0a8}"
ENV RPC_KILL_TIMEOUT 3600
