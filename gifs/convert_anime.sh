#!/bin/bash

INPUT="$1"
FILENAME=$(basename "$INPUT" .mp4)
OUTPUT_DIR="$HOME/Pictures/Wallpapers/gifs"
mkdir -p "$OUTPUT_DIR"

# CONFIGURATION OPTIMISÉE
START_TIME="00:00:05" # Début à 5s (souvent mieux que le début noir)
DURATION="6"          # 6 secondes de loop
FPS="24"
WIDTH="1280"

FILTERS="fps=$FPS,scale=$WIDTH:-1:flags=lanczos"

echo "Conversion de $FILENAME (Segment de ${DURATION}s)..."

# Étape 1 : Générer la palette sur le segment précis
ffmpeg -ss "$START_TIME" -t "$DURATION" -i "$INPUT" -vf "$FILTERS,palettegen" -y /tmp/palette.png

# Étape 2 : Générer le GIF
ffmpeg -ss "$START_TIME" -t "$DURATION" -i "$INPUT" -i /tmp/palette.png \
    -lavfi "$FILTERS [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=3" \
    -loop 0 -an "$OUTPUT_DIR/$FILENAME.gif"

echo "Terminé ! Taille du fichier : $(du -h "$OUTPUT_DIR/$FILENAME.gif" | cut -f1)"
