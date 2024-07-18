#!/bin/bash

tag=$1
bin_root_folder=$2

export PROTOC=$(which protoc) && cargo install --git https://github.com/ankitects/anki.git --tag $tag --root $bin_root_folder anki-sync-server
