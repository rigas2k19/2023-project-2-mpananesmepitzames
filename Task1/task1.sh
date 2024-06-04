#!/bin/bash

# URL="http://127.0.0.1:8000/"   # local
URL="http://project-2.csec.chatzi.org:8000"
USERNAME="%08x.%08x.%08x.%08x.%08x%s%s:"

OUTPUT=$(curl -s -I "$URL" --user "$USERNAME")

IFS=$'\n' read -d '' -ra parts <<< "$OUTPUT"
last_index=$((${#parts[@]}))  # Get the index of the last element

for part in "${parts[@]}"; do
    IFS=':' read -ra substrings <<< "$part"

    for index in "${!substrings[@]}"; do
        if [[ index -eq last_index ]]; then
            substring="${substrings[index]}"
            echo ""
            echo ""
            echo "============================================== TASK 1 =============================================="
            echo ""
            echo ""
            echo "1. MD5 digest : \"$substring"
        fi
    done
done