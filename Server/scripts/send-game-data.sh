#!/bin/bash

lat=${1:-10}
long=${2:-10}
uid=${3:-0}
data="{\"lat\": $lat, \"long\": $long, \"user-id\": $uid}"
server="http://localhost:5000/game_data"

echo "Sending: $data"
curl -H "Content-Type: application/json" -X POST -d "$data" $server
