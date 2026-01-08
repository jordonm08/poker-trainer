#!/bin/bash
# Web version launcher for Poker Trainer

cd "$(dirname "$0")"

echo "Starting Poker Trainer Web Server..."
echo "Once started, open your browser to: http://localhost:5000"
echo ""

python3 -m src.web.app
