FROM grey.ctf/evm-infra

COPY ./contracts /tmp/contracts
COPY ./foundry.toml /tmp/foundry.toml

ENV PORT 30401
ENV HTTP_PORT 30402
ENV PUBLIC_IP "challs.nusgreyhats.org"
ENV FLAG "grey{rounding_is_dangerous_752aa6bb8b6a9f61}"
ENV RPC_KILL_TIMEOUT 3600
