#!/usr/bin/env bash
# auth-with-token.sh — one-shot Gumroad CLI login from a token file
# Usage: bash auth-with-token.sh <token-file>
#   token file = plain text file containing ONLY the access token
#   (Gumroad generates these at gumroad.com -> Settings -> Advanced -> Application form)
set -u
GUM="C:/Users/asus/.local/bin/gumroad.exe"
[ $# -ge 1 ] && [ -s "$1" ] || { echo "usage: bash auth-with-token.sh <token-file>"; exit 1; }
"$GUM" auth login --with-token < "$1" && "$GUM" auth status
