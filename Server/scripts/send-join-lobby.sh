#!/bin/bash

lat=${1:-10}
long=${2:-10}
data="{\"lat\": $lat, \"long\": $long}"
server="http://localhost:5000/join_lobby"

echo "Sending: $data"
curl -H "Content-Type: application/json" -X POST -d "$data" $server
