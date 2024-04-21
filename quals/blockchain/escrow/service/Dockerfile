FROM grey.ctf/evm-infra

COPY ./contracts /tmp/contracts
COPY ./foundry.toml /tmp/foundry.toml

ENV PORT 30101
ENV HTTP_PORT 30102
ENV PUBLIC_IP "challs.nusgreyhats.org"
ENV FLAG "grey{cwia_bytes_overlap_5a392abcfa2d040a}"
ENV RPC_KILL_TIMEOUT 3600
