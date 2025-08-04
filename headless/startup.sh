#!/bin/bash
DATA_FOLDER=/data
ANKICONNECT_CONFIG_FILE=$DATA_FOLDER/addons21/AnkiConnectDev/config.json

mkdir -p $DATA_FOLDER/addons21
ln -s -f /app/anki-connect/plugin $DATA_FOLDER/addons21/AnkiConnectDev

echo "[i] Setting AnkiConnect wildcard webCorsOriginList and webBindAddress!"
jq '.webCorsOriginList = ["*"] | .webBindAddress = "0.0.0.0"' $ANKICONNECT_CONFIG_FILE >tmp_file
mv tmp_file $ANKICONNECT_CONFIG_FILE

if [ -n "$ANKICONNECT_API_KEY" ]; then
    echo "[i] Setting AnkiConnect API key!"
    jq --arg key "$ANKICONNECT_API_KEY" '.apiKey = $key' "$ANKICONNECT_CONFIG_FILE" >tmp_file
    mv tmp_file $ANKICONNECT_CONFIG_FILE
fi

anki -b /data
