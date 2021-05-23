#!/bin/bash

### Generate the appropriate configuration files.
echo "Configuring..."

# User credentials: JSON blob loaded verbatim from environment variable.
if [ "$CREDENTIALS" == "" ]; then
  echo "CREDENTIALS variable not set; failing"
  sleep 10
  exit 1
fi
mkdir -p /root/.config/google-oauthlib-tool
echo $CREDENTIALS > credentials.json
cp credentials.json /root/.config/google-oauthlib-tool/credentials.json

# Device configuration: generated from multiple environment variables based on a template.
if [ "$MODEL_ID" == "" ]; then
  echo "MODEL_ID variable not set; failing"
  sleep 10
  exit 1
fi
if [ "$DEVICE_ID" == "" ]; then
  echo "DEVICE_ID variable not set; failing"
  sleep 10
  exit 1
fi
mkdir -p /root/.config/googlesamples-assistant
cat ./device_config.json.template | sed "s/DEVICE_ID_GOES_HERE/$DEVICE_ID/" | sed "s/MODEL_ID_GOES_HERE/$MODEL_ID/" > device_config.json
cp device_config.json /root/.config/googlesamples-assistant/device_config.json


### Set some basic settings.
echo "Setting volumes"
amixer sset Speaker 75%
amixer sset Mic 75%

### We're ready!
python ./app.py

### We expect the program above to run forever; if it didn't, freeze the app for debugging.
echo "Service crashed!?"
sleep infinity