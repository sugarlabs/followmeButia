#!/bin/bash
cd lua
./lua bobot-server.lua&
cd ../pythonAPI
./waitforbobot.py
sugar-activity -a $SUGAR_ACTIVITY_ID activity.Activity
kill `ps ax | grep bobot-server | grep -v grep | awk '{print $1}'`
