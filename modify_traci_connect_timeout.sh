#!/bin/bash
traci_path=$(pip show traci | grep Location | cut -d ' ' -f 2)/traci/main.py
if [ ! -z $traci_path ]; then
    if [ -z "$(grep 'waitBetweenRetries \*= 2' $traci_path)" ]; then
        sed -i '/time\.sleep(waitBetweenRetries)/a\                waitBetweenRetries \*= 2' $traci_path
    fi
fi
