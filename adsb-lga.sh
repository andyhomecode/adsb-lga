#!/bin/bash

PYTHON_PATH="/home/andy/code/adsb-lga/.venv/bin/python"
SCRIPT_PATH="/home/andy/code/adsb-lga/adsb-lga.py"

while true; do
    output=$($PYTHON_PATH $SCRIPT_PATH --flight)
    if [ -z "$output" ]; then
        echo -n "*"
    else
        echo ""
        echo "$output" | figlet
    fi
    sleep 5
    output=$($PYTHON_PATH $SCRIPT_PATH --airline)
    if [ -z "$output" ]; then
        echo -n "*"
    else
        echo ""
        echo "$output" | figlet
    fi
    sleep 5
    output=$($PYTHON_PATH $SCRIPT_PATH --route)
    if [ -z "$output" ]; then
        echo -n "*"
    else
        echo ""
        echo "$output" | figlet
    fi
    sleep 5
done