FROM rust:1.88.0 AS builder

ARG TAG

ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /build

RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v27.2/protoc-27.2-linux-x86_64.zip && unzip protoc-27.2-linux-x86_64.zip && mv bin/protoc /usr/local/bin/protoc
RUN rustup toolchain uninstall stable && rustup toolchain install stable
RUN rustup update stable 
RUN export PROTOC=$(which protoc) && cargo install --git https://github.com/ankitects/anki.git --tag $TAG --root /build anki-sync-server

FROM gcr.io/distroless/cc-debian12:nonroot

ENV TZ=UTC \
    PASSWORDS_HASHED=1 \
    SYNC_BASE=/data

COPY --from=builder /build/bin/anki-sync-server /usr/local/bin/anki-sync-server

EXPOSE 8080

CMD ["/usr/local/bin/anki-sync-server"]
