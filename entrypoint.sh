#!/bin/sh
set -e

webhook=$1
title=$2
message=$3

python3 /send_adaptive_card.py "$webhook" "$title" "$message"
