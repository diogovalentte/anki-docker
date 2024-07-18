FROM python:3.10

WORKDIR /app

COPY . .

RUN apt update && apt upgrade -y
RUN apt install -y wget unzip
RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v27.2/protoc-27.2-linux-x86_64.zip && unzip protoc-27.2-linux-x86_64.zip && mv bin/protoc /usr/local/bin/protoc
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
RUN mkdir -p /data/config && \
    echo '[net]\ngit-fetch-with-cli = true' | tee ~/.cargo/config.toml
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x install_anki_sync_server.sh

ENV TZ=UTC \
    NTFY_ADDRESS=\
    NTFY_TOPIC=\
    NTFY_TOKEN=\
    GITHUB_TOKEN=\
    PATH="/root/.cargo/bin:${PATH}" \
    CONFIG_FOLDER=/data/config \
    ANKI_STORAGE_FOLDER=/data/anki

EXPOSE 8080

ENTRYPOINT ["python", "main.py"]
