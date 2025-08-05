#!/bin/bash
DATA_FOLDER=/data
ANKICONNECTION_FOLDER=$DATA_FOLDER/addons21/AnkiConnectDev
ANKICONNECT_CONFIG_FILE=$ANKICONNECTION_FOLDER/config.json

mkdir -p $DATA_FOLDER/addons21
rm -rf $ANKICONNECTION_FOLDER
cp -r -a /app/anki-connect/plugin $ANKICONNECTION_FOLDER

echo "[i] Setting AnkiConnect wildcard webCorsOriginList and webBindAddress!"
jq '.webCorsOriginList = ["*"] | .webBindAddress = "0.0.0.0"' $ANKICONNECT_CONFIG_FILE >tmp_file
mv tmp_file $ANKICONNECT_CONFIG_FILE

if [ -n "$ANKICONNECT_API_KEY" ]; then
    echo "[i] Running protected AnkiConnect with API key!"
    anki -b $DATA_FOLDER &
    ANKI_PID=$!

    sleep 5
    if ! kill -0 "$ANKI_PID" 2>/dev/null; then
        echo "[!] Anki not started yet. Not starting proxy server."
        exit 1
    fi

    echo "[i] Anki is running, starting proxy server!"
    exec uvicorn proxy:app --host 0.0.0.0 --port 8766
    exit 0
else
    echo "[i] Running unprotected AnkiConnect!"
    anki -b $DATA_FOLDER
fi
