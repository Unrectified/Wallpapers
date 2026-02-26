#!/bin/bash

# 1. On récupère juste le nom du fichier (ex: castle-of-shadows) sans le chemin ni l'extension
FILENAME=$(basename "$1" .mp4)
OUTPUT_DIR="$HOME/Pictures/Wallpapers/gifs"

# 2. On s'assure que le dossier de destination existe
mkdir -p "$OUTPUT_DIR"

# 3. Commande FFmpeg corrigée
# Note : On utilise $HOME au lieu de ~ pour éviter les soucis de guillemets
ffmpeg -i "$1" \
    -vcodec libwebp \
    -filter:v "fps=30,scale=1920:-1" \
    -lossless 0 -compression_level 6 -q:v 75 -loop 0 -an \
    "$OUTPUT_DIR/$FILENAME.gif"
