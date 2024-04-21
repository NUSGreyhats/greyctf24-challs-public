FROM rust:latest as builder
WORKDIR /app
COPY . .

RUN cargo build --release --bin fearless-concurrency


FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y libssl-dev pkg-config
RUN apt-get install -y ca-certificates
WORKDIR /app
COPY --from=builder /app/target/release/fearless-concurrency /usr/local/bin
ENTRYPOINT ["/usr/local/bin/fearless-concurrency"]