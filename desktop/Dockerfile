FROM lsiobase/kasmvnc:ubuntunoble

ARG ANKI_VERSION

RUN \
  apt-get update && \
  apt-get install -y anki mplayer wget zstd xdg-utils libxcb-xinerama0 libxcb-cursor0 && \
  dpkg --remove anki && \
  wget https://github.com/ankitects/anki/releases/download/${ANKI_VERSION}/anki-${ANKI_VERSION}-linux-x86_64.tar.zst && \
  tar --use-compress-program=unzstd -xvf anki-${ANKI_VERSION}-linux-x86_64.tar.zst && \
  cd anki-linux && ./install.sh &&  cd .. && \
  rm -rf anki-linux anki-${ANKI_VERSION}-linux-x86_64.tar.zst && \
  apt-get clean && \
  mkdir -p /config/app/Anki2 && \
  mkdir -p /config/app/Anki && \
  mkdir -p /config/.local/share && \
  ln -s /config/app/Anki  /config/.local/share/Anki  && \
  ln -s /config/app/Anki2 /config/.local/share/Anki2

VOLUME "/config/app" 

COPY ./root /
