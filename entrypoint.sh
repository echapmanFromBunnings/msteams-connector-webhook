#!/bin/sh

export webhook=$1
export title=$2
export message=$3

cat << EOF > webhook.py
#!/usr/bin/python3
import pymsteams
import sys

webhook = sys.argv[1]
title = sys.argv[2]
message = sys.argv[3]

myTeamsMessage = pymsteams.connectorcard(webhook)
myTeamsMessage.title(title)
myTeamsMessage.text(message)
myTeamsMessage.printme()
myTeamsMessage.send()

EOF

chmod 755 webhook.py

./webhook.py $webhook "$title" "$message"
