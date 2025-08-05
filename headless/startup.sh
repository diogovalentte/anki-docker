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
    echo "[i] Setting AnkiConnect API key!"
    jq --arg key "$ANKICONNECT_API_KEY" '.apiKey = $key' "$ANKICONNECT_CONFIG_FILE" >tmp_file
    mv tmp_file $ANKICONNECT_CONFIG_FILE
fi

anki -b $DATA_FOLDER
