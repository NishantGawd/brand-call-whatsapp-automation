#!/usr/bin/env bash

set -e

echo "=== Checking development environment ==="

echo -n "Python version: "
python --version 2>/dev/null || python3 --version || { echo "Python not installed"; exit 1; }

echo -n "Node version: "
node -v || { echo "Node.js not installed"; exit 1; }

echo -n "npm version: "
npm -v || { echo "npm not installed"; exit 1; }

echo -n "Git version: "
git --version || { echo "Git not installed"; exit 1; }

echo -n "Docker version: "
docker -v || { echo "Docker not installed"; exit 1; }

echo -n "Docker Compose version: "
docker compose version || { echo "docker compose not available"; exit 1; }

echo "Environment looks OK for development."
