FROM debian:12.4-slim

ARG ANKI_VERSION
ARG ANKICONNECT_VERSION

# Innitial setup
RUN apt update && apt install --no-install-recommends -y \
        wget zstd mpv locales curl git ca-certificates jq libxcb-xinerama0 libxcb-cursor0 libnss3 \
        libxcomposite-dev libxdamage-dev libxtst-dev libxkbcommon-dev libxkbfile-dev libatomic1 && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m anki

# Anki installation
RUN mkdir /app && chown -R anki /app
WORKDIR /app
COPY startup.sh .

RUN wget -O ANKI.tar.zst --no-check-certificate https://github.com/ankitects/anki/releases/download/${ANKI_VERSION}/anki-launcher-${ANKI_VERSION}-linux.tar.zst && \
    zstd -d ANKI.tar.zst && rm ANKI.tar.zst && \
    tar xfv ANKI.tar && rm ANKI.tar
WORKDIR /app/anki-launcher-${ANKI_VERSION}-linux

# Run modified install.sh
RUN sed -i 's/xdg-mime/# xdg-mime/' install.sh && sh install.sh

# Post process
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8 \ LANGUAGE=en_US \ LC_ALL=en_US.UTF-8

# Plugin installation
WORKDIR /app
RUN curl -L https://git.sr.ht/~foosoft/anki-connect/archive/${ANKICONNECT_VERSION}.tar.gz | \
    tar -xz && \
    mv anki-connect-${ANKICONNECT_VERSION} anki-connect
RUN chown -R anki:anki /app/anki-connect/plugin
    
EXPOSE 8765
USER anki

ENV QMLSCENE_DEVICE=softwarecontext
ENV FONTCONFIG_PATH=/etc/fonts
ENV QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb
ENV QT_QPA_PLATFORM=vnc
ENV ANKICONNECT_API_KEY=
# Could also use "offscreen"

CMD ["/bin/bash", "startup.sh"]
